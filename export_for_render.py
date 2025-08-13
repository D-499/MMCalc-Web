#!/usr/bin/env python3
"""
Export script for Render deployment
Run this to prepare all files for deployment
"""

import os
import shutil
import zipfile

def create_deployment_package():
    """Create a deployment-ready package for Render"""
    
    # Files to include in the deployment
    files_to_copy = [
        'app.py',
        'calculator.py', 
        'compound_library.py',
        'models.py',
        'main.py',
        'runtime.txt',
        'render.yaml'
    ]
    
    folders_to_copy = [
        'templates',
        'static'
    ]
    
    # Create deployment folder
    deploy_folder = 'mmcalc_deploy'
    if os.path.exists(deploy_folder):
        shutil.rmtree(deploy_folder)
    os.makedirs(deploy_folder)
    
    print("Creating deployment package...")
    
    # Copy files
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, deploy_folder)
            print(f"✓ Copied {file}")
        else:
            print(f"⚠ Warning: {file} not found")
    
    # Copy folders
    for folder in folders_to_copy:
        if os.path.exists(folder):
            shutil.copytree(folder, os.path.join(deploy_folder, folder))
            print(f"✓ Copied {folder}/ folder")
        else:
            print(f"⚠ Warning: {folder}/ folder not found")
    
    # Create requirements.txt (rename from requirements_render.txt)
    if os.path.exists('requirements_render.txt'):
        shutil.copy2('requirements_render.txt', os.path.join(deploy_folder, 'requirements.txt'))
        print("✓ Created requirements.txt")
    else:
        print("⚠ Warning: requirements_render.txt not found")
    
    # Copy deployment guide
    if os.path.exists('DEPLOYMENT_GUIDE.md'):
        shutil.copy2('DEPLOYMENT_GUIDE.md', deploy_folder)
        print("✓ Copied deployment guide")
    
    # Create a zip file for easy upload
    zip_filename = 'mmcalc_for_render.zip'
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(deploy_folder):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, deploy_folder)
                zipf.write(file_path, arcname)
    
    print(f"\n🎉 Deployment package created!")
    print(f"📁 Folder: {deploy_folder}/")
    print(f"📦 Zip file: {zip_filename}")
    print(f"\nNext steps:")
    print(f"1. Upload the contents of '{deploy_folder}' to a GitHub repository")
    print(f"2. Follow the instructions in DEPLOYMENT_GUIDE.md")
    print(f"3. Deploy on Render using the repository")

if __name__ == "__main__":
    create_deployment_package()