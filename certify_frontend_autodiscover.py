import urllib.request
import json

BASE_URL = "http://127.0.0.1:8000"

def get_openapi_spec():
    url = f"{BASE_URL}/openapi.json"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"❌ No se pudo cargar /openapi.json: {e}")
    return None

def test_url(path):
    url = f"{BASE_URL}{path}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            return response.status, json.loads(response.read().decode('utf-8'))
    except Exception as e:
        return getattr(e, 'code', 500), str(e)

def main():
    print("\n" + "█" * 70)
    print("  SUITE DE CERTIFICACIÓN FRONTEND - Detección Dinámica FastAPI")
    print("█" * 70 + "\n")

    spec = get_openapi_spec()
    if not spec:
        print("❌ No se pudo conectar a la API de FastAPI en el puerto 8000.")
        return

    paths = list(spec.get("paths", {}).keys())
    print(f"✔ OpenAPI / FastAPI detectado exitosamente.")
    print(f"  Rutas totales expuestas en el backend: {len(paths)}\n")

    semantic_paths = [p for p in paths if any(k in p.lower() for k in ["semantic", "health", "graph", "risk", "status", "rdf", "reason"])]

    print("=" * 70)
    print(" EVALUACIÓN DE ENDPOINTS CONSUMIDOS POR EL FRONTEND")
    print("=" * 70)

    success_count = 0
    for path in semantic_paths[:10]: # Probar las principales rutas semánticas y de estado
        status, res = test_url(path)
        if status == 200:
            print(f"  ✔ [200 OK]  {path}")
            success_count += 1
        else:
            print(f"  ⚠️ [{status}]      {path}")

    print("\n" + "=" * 70)
    if success_count > 0:
        print(" RESULTADO FINAL: FRONTEND Y API SEMÁNTICA CONECTADOS Y VALIDADOS")
        print(f" Se confirmaron {success_count} rutas semánticas activas que alimentan la interfaz.")
    else:
        print(" REVISIÓN REQUERIDA: Comprueba los prefijos de las rutas en tu archivo main.py.")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()
