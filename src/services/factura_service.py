import re
from PyPDF2 import PdfReader
from src.services.groq_service import valid_products

def get_cufe_code(text: str) -> str:
    m_cufe = re.search(r"Código Único de Factura - CUFE[\s:]+([0-9a-fA-F]{90,100})", text)
    return str(m_cufe.group(1)) if m_cufe else "not found"

def get_date(text: str) -> str:
    m_date = re.search(r"Fecha de Emisión:[\s]+(\d{2}/\d{2}/\d{4})", text)
    return str(m_date.group(1)) if m_date else "not found"

def get_nit(text: str) -> str:
    m_nit = re.search(r"Nit del Emisor:[\s]+([\d\-]+)", text)
    return str(m_nit.group(1)) if m_nit else "not found"

def get_total(text: str) -> str:
    # Match 'Total factura (=)' followed by whitespace, invisible chars (\u3164), C, O, P, or $
    m_totals = list(re.finditer(r"Total factura \(=\)[\s\u3164COP$]+([\d\.,]+)", text))
    if m_totals:
        return str(m_totals[-1].group(1))
    return "not found"

def get_products(text: str) -> list:
    start_match = re.search(r"Detalles de Productos[\s\S]*?(?=\n1\n)", text)
    if not start_match: return []
    start_idx = start_match.end()
    
    ends = [text.find("Notas Finales", start_idx), 
            text.find("Datos Totales", start_idx),
            text.find("Hoja 1 de", start_idx)]
    valid_ends = [e for e in ends if e != -1]
    end_idx = min(valid_ends) if valid_ends else len(text)
    
    prod_blob = text[start_idx:end_idx]
    lines = [L.strip() for L in prod_blob.splitlines() if L.strip() != ""]
    
    items = []
    current_item = []
    expected_nro = 1
    
    for line in lines:
        if line == str(expected_nro):
            if current_item:
                items.append(current_item)
            current_item = [line]
            expected_nro += 1
        elif current_item:
            current_item.append(line)
            
    if current_item:
        items.append(current_item)
        
    products = []
    for item in items:
        valores = []
        rest = []
        for line in reversed(item[1:]):
            if re.match(r'^[\d\.,]+$', line) and (',' in line or '.' in line):
                valores.insert(0, line)
            elif line in ["$", "COP"] or not line:
                pass 
            else:
                rest.insert(0, line)
                
        desc_parts = rest[:-1] if rest else []
        start_idx_desc = 0
        for i, p in enumerate(desc_parts):
            if " " not in p and len(p) <= 10 and i < 2:
                start_idx_desc = i + 1
            else:
                break
                
        desc = "".join(desc_parts[start_idx_desc:]) if desc_parts else "desconocido"
        cantidad = valores[0] if len(valores) > 0 else "0,00"
        costo = valores[1] if len(valores) > 1 else "0,00"
        
        # Format for postgres: remove thousands dots and replace decimal comma with dot
        cantidad = cantidad.replace(".", "").replace(",", ".")
        costo = costo.replace(".", "").replace(",", ".")

        products.append({
            "producto": desc,
            "cantidad": cantidad,
            "costo": costo
        })
        #print(desc)
        #print(cantidad)
        #print(costo)

    return products

def get_all(pdf_path):
    reader = PdfReader(pdf_path)
    
    # Extract text from all pages once for efficiency
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
        
    cufe_code = get_cufe_code(text)
    date = get_date(text)
    nit = get_nit(text)
    total = get_total(text)
    products = get_products(text)
    
    if total != "not found":
        total = total.replace(".", "").replace(",", ".")
        
    return cufe_code, date, nit, total, products


def get_products_from_pdf(pdf_path: str) -> list:
    data = get_all(pdf_path)
    valid_list = valid_products(data[4])
    print(valid_list)
    return valid_list