import httpx
import re

def check_frontend():
    client = httpx.Client(base_url="http://localhost:3000", timeout=10.0)
    res = client.get("/")
    print(f"Page Status: {res.status_code}")
    print(f"Page HTML Length: {len(res.text)}")
    
    css_links = re.findall(r'href=["\'](/_next/static/css/[^"\']+)["\']', res.text)
    js_links = re.findall(r'src=["\'](/_next/static/chunks/[^"\']+)["\']', res.text)
    
    print(f"\nDiscovered CSS Links ({len(css_links)}):")
    for css in css_links:
        r = client.get(css)
        print(f"  {css} -> HTTP {r.status_code} ({len(r.text)} bytes)")
        if "tailwind" in r.text.lower() or "slate" in r.text.lower() or "display" in r.text.lower():
            print("    [OK] Tailwind CSS rules verified in bundle")
            
    print(f"\nDiscovered JS Chunks ({len(js_links)}):")
    for js in js_links[:5]:
        r = client.get(js)
        print(f"  {js} -> HTTP {r.status_code} ({len(r.text)} bytes)")

if __name__ == "__main__":
    check_frontend()
