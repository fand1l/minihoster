from django.shortcuts import render
from django.http import JsonResponse

from .forms import MinecraftServerForm
from control_panel.models import MinecraftServer

from django.views.generic.edit import CreateView

import requests
import os
import xml.etree.ElementTree as ET

class ServerCreateView(CreateView):
    model = MinecraftServer
    form_class = MinecraftServerForm
    template_name = "installing/server_create.html"
    success_url = "/dashboard/"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        
        software = self.request.POST.get("software")
        version = self.request.POST.get("version")
        download_url = self.request.POST.get("download_url")

        final_jar_path = os.path.join(form.instance.server_dir_location, "server.jar")

        try:
            print(f"Завантажуємо {download_url}...")
            response = requests.get(download_url)
            response.raise_for_status()
            
            jar_data = response.content

            os.makedirs(form.instance.server_dir_location, exist_ok=True)

            with open(final_jar_path, "wb") as f:
                f.write(jar_data)
            print(f"Файл збережено: {final_jar_path}")

        except requests.exceptions.RequestException as e:
            form.add_error(None, f"Download file error: {e}")
            return super().form_invalid(form)
        except OSError as e:
            form.add_error(None, f"Save file error: {e}")
            return super().form_invalid(form)

        form.instance.software = software
        form.instance.version = version
        form.instance.jar_path = final_jar_path
        
        return super().form_valid(form)
    

def get_available_versions(request):
    software_name = request.GET.get("software")

    if not software_name:
        return JsonResponse({"error": "No software"}, status=400)
    
    versions_list = []

    if software_name == "vanilla":
        try:
            api_url = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
            response = requests.get(api_url)
            response.raise_for_status()

            data = response.json()
            versions_list = []
            for i in data["versions"]:
                versions_list.append(i["id"])
        
        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": str(e)}, status=503)
        except KeyError:
            return JsonResponse({"error": "API dead"}, status=500)

    
    if software_name == "paper":
        try:
            api_url = "https://api.papermc.io/v2/projects/paper/"
            response = requests.get(api_url)
            response.raise_for_status()

            data = response.json()
            versions_list = data["versions"]
        
        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": str(e)}, status=503)
        except KeyError:
            return JsonResponse({"error": "API dead"}, status=500)
        
    
    if software_name == "folia":
        try:
            api_url = "https://api.papermc.io/v2/projects/folia/"
            response = requests.get(api_url)
            response.raise_for_status()

            data = response.json()
            versions_list = data["versions"]
        
        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": str(e)}, status=503)
        except KeyError:
            return JsonResponse({"error": "API dead"}, status=500)
        
    
    if software_name == "velocity":
        try:
            api_url = "https://api.papermc.io/v2/projects/velocity/"
            response = requests.get(api_url)
            response.raise_for_status()

            data = response.json()
            versions_list = data["versions"]
        
        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": str(e)}, status=503)
        except KeyError:
            return JsonResponse({"error": "API dead"}, status=500)
        
    
    if software_name == "arclight":
        try:
            api_url = "https://api.github.com/repos/IzzelAliz/Arclight/releases"
            response = requests.get(api_url)
            response.raise_for_status()

            data = response.json()

            cleaned_versions = set()

            for release in data:
                for rel in release["assets"]:
                    name = rel["name"]
                    if not name.endswith('.jar') or 'sources' in name or 'javadoc' in name:
                        continue

                    try:
                        parts = name.split('-')
                        modloader = parts[1] # "fabric"
                        version = parts[2]   # "1.20.1"
                        
                        clean_name = f"{version}-{modloader}"
                        cleaned_versions.add(clean_name)
                        
                    except IndexError:
                        pass
            
            versions_list = sorted(list(cleaned_versions), reverse=True)
        
        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": str(e)}, status=503)
        except KeyError:
            return JsonResponse({"error": "API dead"}, status=500)
        
    
    if software_name == "fabric":
        try:
            api_url = "https://meta.fabricmc.net/v2/versions/game"
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()

            versions_list = [v["version"] for v in data]
            
        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": str(e)}, status=503)
        except KeyError:
            return JsonResponse({"error": "API response format error for Fabric"}, status=500)
        
    
    if software_name == "forge":
        try:
            api_url = "https://maven.minecraftforge.net/net/minecraftforge/forge/maven-metadata.xml"
            response = requests.get(api_url)
            response.raise_for_status()
            
            root = ET.fromstring(response.text)
            
            versions_tag = root.find('versioning/versions')
            if versions_tag is not None:
                for v in versions_tag.findall('version'):
                    versions_list.append(v.text)

            versions_list.reverse()

        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": str(e)}, status=503)
        except ET.ParseError:
            return JsonResponse({"error": "API response format error for Forge (XML)"}, status=500)
        
    
    if software_name == "neoforge":
        try:
            api_url = "https://maven.neoforged.net/net/neoforged/neoforge/maven-metadata.xml"
            response = requests.get(api_url)
            response.raise_for_status()
            
            root = ET.fromstring(response.text)
            versions_tag = root.find('versioning/versions')
            if versions_tag is not None:
                for v in versions_tag.findall('version'):
                    versions_list.append(v.text)
            
            versions_list.reverse()

        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": str(e)}, status=503)
        except ET.ParseError:
            return JsonResponse({"error": "API response format error for NeoForge (XML)"}, status=500)
        
    
    if software_name == "quilt":
        try:
            api_url = "https://meta.quiltmc.org/v3/versions/game"
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()

            versions_list = [v["version"] for v in data]
            
        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": str(e)}, status=503)
        except KeyError:
            return JsonResponse({"error": "API response format error for Quilt"}, status=500)
        
    
    return JsonResponse({"versions": versions_list})


def get_download_info(request):
    software_name = request.GET.get("software")
    version = request.GET.get("version")
    file_name = ""
    download_url = ""

    if not software_name or not version:
        return JsonResponse({"error": "No software or version"}, status=400)
    
    if software_name == "vanilla":
        try:
            api_url = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
            response = requests.get(api_url)
            response.raise_for_status()

            data = response.json()
            for i in data["versions"]:
                if i["id"] == version:
                    api_url = i["url"]

            response = requests.get(api_url)
            response.raise_for_status()

            data = response.json()
            download_url = data["downloads"]["server"]["url"]
            file_name = "server.jar"
            

        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": str(e)}, status=503)
        except KeyError:
            return JsonResponse({"error": "API dead"}, status=500)
    

    if software_name == "paper":
        try:
            api_url = f"https://api.papermc.io/v2/projects/paper/versions/{version}"
            response = requests.get(api_url)
            response.raise_for_status()

            data = response.json()
            latest_build = data["builds"][-1]

            api_url = f"https://api.papermc.io/v2/projects/paper/versions/{version}/builds/{latest_build}"
            response = requests.get(api_url)
            response.raise_for_status()

            data = response.json()
            file_name = data["downloads"]["application"]["name"]
            download_url = f"https://api.papermc.io/v2/projects/paper/versions/{version}/builds/{latest_build}/downloads/{file_name}"
        
        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": str(e)}, status=503)
        except KeyError:
            return JsonResponse({"error": "API dead"}, status=500)
        
    
    if software_name == "folia":
        try:
            api_url = ""
            response = requests.get(api_url)
            response.raise_for_status()

            data = response.json()
            latest_build = data["builds"][-1]

            api_url = f"https://api.papermc.io/v2/projects/folia/versions/{version}/builds/{latest_build}"
            response = requests.get(api_url)
            response.raise_for_status()

            data = response.json()
            file_name = data["downloads"]["application"]["name"]
            download_url = f"https://api.papermc.io/v2/projects/folia/versions/{version}/builds/{latest_build}/downloads/{file_name}"

        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": str(e)}, status=503)
        except KeyError:
            return JsonResponse({"error": "API dead"}, status=500)
        
    
    if software_name == "velocity":
        try:
            api_url = ""
            response = requests.get(api_url)
            response.raise_for_status()

            data = response.json()
            latest_build = data["builds"][-1]

            api_url = f"https://api.papermc.io/v2/projects/velocity/versions/{version}/builds/{latest_build}"
            response = requests.get(api_url)
            response.raise_for_status()

            data = response.json()
            file_name = data["downloads"]["application"]["name"]
            download_url = f"https://api.papermc.io/v2/projects/velocity/versions/{version}/builds/{latest_build}/downloads/{file_name}"

        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": str(e)}, status=503)
        except KeyError:
            return JsonResponse({"error": "API dead"}, status=500)
        

    if software_name == "arclight":
        try:
            api_url = ""
            response = requests.get(api_url)
            response.raise_for_status()

            data = response.json()

        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": str(e)}, status=503)
        except KeyError:
            return JsonResponse({"error": "API dead"}, status=500)
        
    
    if software_name == "fabric":
        try:
            api_url = ""
            response = requests.get(api_url)
            response.raise_for_status()

            data = response.json()

        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": str(e)}, status=503)
        except KeyError:
            return JsonResponse({"error": "API dead"}, status=500)
        

    if software_name == "forge":
        try:
            api_url = ""
            response = requests.get(api_url)
            response.raise_for_status()

            data = response.json()

        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": str(e)}, status=503)
        except KeyError:
            return JsonResponse({"error": "API dead"}, status=500)
        

    if software_name == "neoforge":
        try:
            api_url = ""
            response = requests.get(api_url)
            response.raise_for_status()

            data = response.json()

        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": str(e)}, status=503)
        except KeyError:
            return JsonResponse({"error": "API dead"}, status=500)
        

    if software_name == "quilt":
        try:
            api_url = ""
            response = requests.get(api_url)
            response.raise_for_status()

            data = response.json()

        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": str(e)}, status=503)
        except KeyError:
            return JsonResponse({"error": "API dead"}, status=500)
        
        
    return JsonResponse({"file_name": file_name, "download-url": download_url})
        
        
