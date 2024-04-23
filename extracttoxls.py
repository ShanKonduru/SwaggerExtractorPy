import requests
import pandas as pd
from swagger_parser import SwaggerParser

import yaml

def parse_swagger(url):
    response = requests.get(url)
    print("Response Status Code:", response.status_code)
    print("Response Content:", response.text)
    if response.status_code != 200:
        print("Failed to retrieve Swagger spec:", response.status_code)
        return None
    
    # Parse YAML content
    swagger_spec = yaml.safe_load(response.text)

    # Save YAML content to a file
    with open('swagger.yaml', 'w') as f:
        yaml.dump(swagger_spec, f)

    # Return file path
    return 'swagger.yaml'

def extract_info(swagger_parser):
    paths = swagger_parser.paths
    endpoints = []

    for path, path_info in paths.items():
        for method, method_info in path_info.items():
            endpoint = {
                'Path': path,
                'Method': method.upper(),
                'Description': method_info.get('summary', ''),
                'Parameters': ', '.join([param['name'] for param in method_info.get('parameters', [])]),
                'Responses': ', '.join([str(code) for code in method_info.get('responses', {}).keys()])
            }
            endpoints.append(endpoint)
    
    return endpoints

def export_to_excel(data, filename):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)

def export_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

def main():
    swagger_url = input("Enter Swagger URL: ")
    swagger_path = parse_swagger(swagger_url)
    if swagger_path:
        swagger_parser = SwaggerParser(swagger_path)
        data = extract_info(swagger_parser)
        export_format = input("Enter export format (csv/excel): ").lower()
        if export_format == "csv":
            filename = input("Enter CSV filename: ")
            export_to_csv(data, filename)
            print("Data exported to", filename)
        elif export_format == "excel":
            filename = input("Enter Excel filename: ")
            export_to_excel(data, filename)
            print("Data exported to", filename)
        else:
            print("Invalid export format. Please choose either 'csv' or 'excel'.")

if __name__ == "__main__":
    main()
