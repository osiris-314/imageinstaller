#!/usr/bin/env python3
import subprocess
from colorama import Fore
import os
import os.path
import sys
import time

def list_disks():
    result = subprocess.run(['lsblk', '-o', 'NAME,RM,TYPE,SIZE'], stdout=subprocess.PIPE, text=True)
    lines = result.stdout.strip().split('\n')
    headers = lines[0].split()
    disks_info = lines[1:]
    disks = []

    for disk in disks_info:
        disk_data = disk.split()
        name = disk_data[0]
        removable = disk_data[1]
        dtype = disk_data[2]
        size = disk_data[3]
        
        if dtype == 'disk':
            is_removable = "Yes" if removable == '1' else "No"
            disk_info = (f"/dev/{name}", size, is_removable)
            disks.append(disk_info)
    
    return disks

def display_os_options():
    os_options = {
        1: "Ubuntu",
        2: "Kali",
        4: "Parrot"
    }
    os.system('clear')
    print(Fore.LIGHTBLUE_EX + "Select Operating System:" + Fore.RESET)
    for i, os_name in os_options.items():
        print(Fore.LIGHTGREEN_EX + f"{i}. {os_name}" + Fore.RESET)

    os_choice = int(input("Please select an operating system (enter number): "))

    if os_choice in os_options:
        return os_options[os_choice]
    else:
        print(Fore.RED + "Invalid selection. Exiting." + Fore.RESET)
        exit(1)

def display_platform_options(os_selection, images):
    available_platforms = {k: v for k, v in images.get(os_selection, {}).items() if v}
    
    if not available_platforms:
        print(Fore.RED + f"No platforms available for {os_selection}. Exiting." + Fore.RESET)
        exit(1)

    os.system('clear')
    print(Fore.LIGHTBLUE_EX + f"Select Platform for {os_selection}:" + Fore.RESET)
    for i, platform in enumerate(available_platforms.keys(), 1):
        print(Fore.LIGHTGREEN_EX + f"{i}. {platform}" + Fore.RESET)
    
    platform_choice = int(input("Please select a platform (enter number): "))

    if 1 <= platform_choice <= len(available_platforms):
        return list(available_platforms.keys())[platform_choice - 1]
    else:
        print(Fore.RED + "Invalid selection. Exiting." + Fore.RESET)
        exit(1)

def display_image_options(os_selection, platform, images):
    available_images = images[os_selection][platform]
    
    if not available_images:
        print(Fore.RED + f"No images available for {os_selection} on {platform}. Exiting." + Fore.RESET)
        exit(1)

    os.system('clear')
    print(Fore.LIGHTBLUE_EX + f"Available Images for {os_selection} - {platform}:" + Fore.RESET)
    for i, image in available_images.items():
        print(Fore.LIGHTGREEN_EX + f"{i}. {image['name']}" + Fore.RESET)
    global image_choice
    image_choice = int(input("Please select an image to download (enter number): "))

    if image_choice in available_images:
        return available_images[image_choice]
    else:
        print(Fore.RED + "Invalid selection. Exiting." + Fore.RESET)
        exit(1)

def download_image(image_name, image_url):
    os.system('clear')
    print(Fore.LIGHTBLUE_EX + 'Downloading Image ' + Fore.LIGHTGREEN_EX + str(image_name) + Fore.LIGHTBLUE_EX + ' ...' + Fore.RESET)
    file_name = image_url.split('/')[-1]
    result = subprocess.run(f'curl -O {image_url}', shell=True)
    
    if result.returncode == 0:
        print(Fore.GREEN + "Download complete!" + Fore.RESET)
        return file_name
    else:
        print(Fore.RED + "Error downloading the image." + Fore.RESET)
        exit(1)

def main():
    keep_file = '-keep' in sys.argv

    images = {
        "Kali": {
            "Raspberry Pi": {
                1: {"name": " Kali Raspberry Pi 1", "url": "https://kali.download/arm-images/kali-2024.2/kali-linux-2024.2-raspberry-pi1-armel.img.xz"},
                2: {"name": " Kali Raspberry Pi 2 32-bit", "url": "https://kali.download/arm-images/kali-2024.2/kali-linux-2024.2-raspberry-pi-armhf.img.xz"},
                3: {"name": " Kali Raspberry Pi 2 64-bit", "url": "https://kali.download/arm-images/kali-2024.2/kali-linux-2024.2-raspberry-pi-arm64.img.xz"},
                4: {"name": " Kali Raspberry Pi 3 32-bit", "url": "https://kali.download/arm-images/kali-2024.2/kali-linux-2024.2-raspberry-pi-armhf.img.xz"},
                5: {"name": " Kali Raspberry Pi 3 64-bit", "url": "https://kali.download/arm-images/kali-2024.2/kali-linux-2024.2-raspberry-pi-arm64.img.xz"},
                6: {"name": " Kali Raspberry Pi 4 32-bit", "url": "https://kali.download/arm-images/kali-2024.2/kali-linux-2024.2-raspberry-pi-armhf.img.xz"},
                7: {"name": " Kali Raspberry Pi 4 64-bit", "url": "https://kali.download/arm-images/kali-2024.2/kali-linux-2024.2-raspberry-pi-arm64.img.xz"},
                8: {"name": " Kali Raspberry Pi 5 64-bit", "url": "https://kali.download/arm-images/kali-2024.2/kali-linux-2024.2-raspberry-pi-armhf.img.xz"},
                9: {"name": " Kali Raspberry Pi Zero W", "url": "https://kali.download/arm-images/kali-2024.2/kali-linux-2024.2-raspberry-pi-zero-w-armel.img.xz"},
                10: {"name": "Kali Raspberry Pi Zero 2 W", "url": "https://kali.download/arm-images/kali-2024.2/kali-linux-2024.2-raspberry-pi-zero-2-w-armhf.img.xz"}
                },
            "Desktop Installer": {
                1: {"name": "Kali Desktop Installer 32-bit", "url": "https://cdimage.kali.org/kali-2024.2/kali-linux-2024.2-installer-i386.iso"},
                2: {"name": "Kali Desktop Installer 64-bit", "url": "https://cdimage.kali.org/kali-2024.2/kali-linux-2024.2-installer-amd64.iso"}
            },
            "Live Boot": {
                1: {"name": "Kali Live Boot 32-bit", "url": "https://cdimage.kali.org/kali-2024.2/kali-linux-2024.2-live-i386.iso"},
                2: {"name": "Kali Live Boot 64-bit", "url": "https://cdimage.kali.org/kali-2024.2/kali-linux-2024.2-live-amd64.iso"}
            }
        },
        "Ubuntu": {
            "Raspberry Pi": {
                1: {"name": " Ubuntu Raspberry Pi 4", "url": "https://cdimage.ubuntu.com/releases/24.04/release/ubuntu-24.04-preinstalled-desktop-arm64+raspi.img.xz"},
                2: {"name": " Ubuntu Raspberry Pi 5", "url": "https://cdimage.ubuntu.com/releases/24.04/release/ubuntu-24.04-preinstalled-desktop-arm64+raspi.img.xz"},
                3: {"name": " Ubuntu Raspberry Pi Zero 2 W", "url": "https://cdimage.ubuntu.com/releases/24.04/release/ubuntu-24.04-preinstalled-desktop-arm64+raspi.img.xz"},
                4: {"name": " Ubuntu Raspberry Pi 400", "url": "https://cdimage.ubuntu.com/releases/24.04/release/ubuntu-24.04-preinstalled-desktop-arm64+raspi.img.xz"}
                },
            "Desktop Installer": {
                1: {"name": "Ubuntu Desktop Installer", "url": "https://releases.ubuntu.com/24.04/ubuntu-24.04-desktop-amd64.iso"}
                },
        },
        "Parrot": {
            "Desktop Installer": {
                1: {"name": "Parrot Desktop Installer", "url":

 "https://cdimage.ubuntu.com/releases/24.04/release/ubuntu-24.04-preinstalled-desktop-arm64+raspi.img.xz"},
                }
        }
    }

    print('\n')

    disks = list_disks()

    for i, disk in enumerate(disks, 1):
        name, size, removable = disk
        if removable == 'Yes':
            rem = 'Removable'
        else:
            rem = 'Non-Removable'
        print(Fore.LIGHTBLUE_EX + str(i) + '. ' + Fore.CYAN + str(name) + Fore.WHITE + ' - ' + Fore.LIGHTGREEN_EX + str(size) + Fore.WHITE + ' - ' + Fore.YELLOW + str(rem) + Fore.RESET)
    global disk_choice
    disk_choice = int(input("Select the disk to install to (enter number): "))

    if 1 <= disk_choice <= len(disks):
        selected_disk = disks[disk_choice - 1][0]
        print(Fore.LIGHTGREEN_EX + f"Selected disk: {selected_disk}" + Fore.RESET)
    else:
        print(Fore.RED + "Invalid selection. Exiting." + Fore.RESET)
        exit(1)

    os_selection = display_os_options()
    platform_selection = display_platform_options(os_selection, images)
    image_selection = display_image_options(os_selection, platform_selection, images)

    os.system('clear')
    wifi_name = input('Type WIFI name: ')
    wifi_pass = input('Type WIFI pass: ')
    os.system('clear')

    downloaded_file = download_image(image_selection["name"], image_selection["url"])

    os.system('clear')
    print(Fore.LIGHTGREEN_EX + 'Successfully Downloaded Image ' + Fore.CYAN + str(image_selection["name"]))
    print(Fore.LIGHTBLUE_EX + 'Installing ' + Fore.LIGHTGREEN_EX + str(image_selection["name"]) + Fore.LIGHTBLUE_EX + ' At ' + Fore.CYAN + str(selected_disk) + Fore.LIGHTBLUE_EX + ' ...' + Fore.RESET)

    subprocess.run(f'xzcat {downloaded_file} | sudo dd of={selected_disk} bs=4M conv=fsync status=progress', shell=True)
    os.system('clear')

    if not keep_file:
        subprocess.run(f'rm {downloaded_file}', shell=True)

    subprocess.run('mkdir /mnt/image_boot',shell=True)
    subprocess.run('mkdir /mnt/image_rootfs',shell=True)
    mnt_boot = '/mnt/image_boot'
    mnt_rootfs = '/mnt_image_rootfs'
    os.system('clear')
    print(Fore.LIGHTBLUE_EX + 'Mounting ' + Fore.LIGHTGREEN_EX + 'BOOT' + Fore.LIGHTBLUE_EX + ' and ' + Fore.LIGHTGREEN_EX + 'ROOTFS' + Fore.LIGHTBLUE_EX + ' to the system' + Fore.RESET)
    subprocess.run(f'sudo mount {selected_disk}1 /mnt/image_boot',shell=True)
    subprocess.run(f'sudo mount {selected_disk}2 /mnt/image_rootfs',shell=True)
    time.sleep(15)
    os.system('clear')

    print(Fore.LIGHTGREEN_EX + 'Successfully Downloaded Image ' + Fore.CYAN + str(image_selection["name"]))
    print(Fore.LIGHTGREEN_EX + 'Successfully Installed Image ' + Fore.CYAN + str(image_selection["name"]) + Fore.LIGHTGREEN_EX + ' At ' + Fore.CYAN + str(selected_disk) + Fore.RESET)


    subprocess.run('sudo touch ssh',shell=True)
    subprocess.run(f'sudo wpa_passphrase {wifi_name} {wifi_pass} > wpa_supplicant.conf',shell=True)
    ssh_file_path = "ssh"
    wpa_supplicant_file_path = "wpa_supplicant.conf"

    subprocess.run(f'sudo cp {ssh_file_path} {mnt_boot}', shell=True)
    print(Fore.LIGHTGREEN_EX + 'SSH Enabled' + Fore.RESET)
    subprocess.run(f'sudo cp {wpa_supplicant_file_path} {mnt_boot}', shell=True)
    print(Fore.LIGHTGREEN_EX + 'WIFI network added' + Fore.RESET)

    subprocess.run('sudo umount /mnt/image_boot',shell=True)
    subprocess.run('sudo umount /mnt/image_rootfs',shell=True)   

    subprocess.run('sudo rm -rf /mnt/image_boot',shell=True)
    subprocess.run('sudo rm -rf /mnt/image_rootfs',shell=True)

if __name__ == "__main__":
    main()
