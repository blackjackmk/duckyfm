# DuckyFM

> Python GUI application with Azure SQL Database


## 📄 About

DuckyFM is a music management application that allows you to manage information about albums, artists, and songs. Users can create, edit, and delete information, as well as assign songs to albums and artists.␍
DuckyFM is designed using modern programming technologies. The application is written in Python and uses the PyQt library to create the user interface. Data is stored in an Azure SQL database, which ensures security and availability from various devices.␍
DuckyFM is the ideal tool for anyone who wants to manage their music collection. Whether you have a small collection of your favorite songs or a large library of music, DuckyFM can help you keep track of everything.

## 🚀 Technologies Used

- Python
- PyQt5
- Microsoft Azure SQL / SQL Server

## 🖼️ Screenshots

<details>
<summary><b>Click to expand screenshots</b></summary>
<br>

![](assets/duckyfm_1.webp)
![](assets/duckyfm_2.webp)
![](assets/duckyfm_3.webp)
![](assets/duckyfm_4.webp)
![](assets/duckyfm_5.webp)
![](assets/duckyfm_6.webp)
![](assets/duckyfm_7.webp)
![](assets/duckyfm_8.webp)
![](assets/duckyfm_9.webp)
![](assets/duckyfm_10.webp)

</details>

## 📦 Installation

1. **Install Python**: Download and install Python from the official website.

2. **Create a Virtual Environment** (Recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install Requirements**: Run `pip install -r requirements.txt` in your command line to install the required dependencies.

4. **Deploy SQL Database**: Set up your SQL Server database either locally or in Microsoft Azure. You only need to create a blank database.

5. **Set Environment Variables**: Set the following environment variables
   - `DB_LOGIN`: _login_to_database_
   - `DB_PASS`: _password_to_database_
   - `DB_SERVER`: _server_adress_
   - `DB_SERVER`: _server_address_
   - `DB_NAME`: _name_of_database_

6. **Initialize Database Schema**: Run `python default_base.py` to connect to your database and automatically generate the required tables and relationships.

7. **Run Application**: Execute `python main.py` in your command line to start DuckyFM.
