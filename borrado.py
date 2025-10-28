import boto3

# Configura la región (ejemplo: Irlanda)
REGION = "eu-west-1"

def clean_lambda_versions():
    client = boto3.client("lambda", region_name=REGION)

    # Listar todas las funciones
    paginator = client.get_paginator("list_functions")
    for page in paginator.paginate():
        for function in page["Functions"]:
            function_name = function["FunctionName"]
            print(f"\n🔍 Revisando función: {function_name}")

            # Listar versiones de la función
            versions = client.list_versions_by_function(FunctionName=function_name)["Versions"]

            # Obtener versiones protegidas por alias
            aliases = client.list_aliases(FunctionName=function_name)["Aliases"]
            protected_versions = {"$LATEST"} | {alias["FunctionVersion"] for alias in aliases}

            for version in versions:
                ver = version["Version"]

                # Saltar versiones protegidas
                if ver in protected_versions:
                    continue

                try:
                    print(f"  🗑️ Eliminando {function_name} versión {ver}")
                    client.delete_function(FunctionName=function_name, Qualifier=ver)
                except Exception as e:
                    print(f"  ⚠️ Error al eliminar {function_name} versión {ver}: {e}")

if __name__ == "__main__":
    clean_lambda_versions()
    print("\n✅ Limpieza completada.")
