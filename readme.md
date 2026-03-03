# LitExplorer: Research Library App

**LitExplorer** is a Streamlit application designed to facilitate the vizualisation and interaction with a database of scientific literature focused on nitrosamines. This project was developed in collaboration with students from **ECPM Strasbourg** to improve access to key information on a subject that has become crucial in the pharmaceutical industry. What sets **LitExplorer** apart is its emphasis on user collaboration: through features like **reviews** and **ratings**, users can share insights, evaluate resources, and collectively enhance the value of the database. This interactive approach not only improves accessibility but also fosters a dynamic exchange of knowledge among researchers and professionals.



## Table of Contents

1. [Introduction](#introduction)
2. [Objectives and Features](#objectives-and-features)
3. [Target Audience](#target-audience)
4. [Technical Requirements](#technical-requirements)
5. [Database Overview](#database-overview)
6. [Installation Guide](#installation-guide)
7. [First Use](#first-use)
8. [Structure and Navigation](#structure-and-navigation)
9. [Customization and Maintenance](#customization-and-maintenance)
10. [Developer and Contributions](#developer-and-contributions)
11. [Future Work](#future-work)

## Objectives and Features

#### Objectives

LitExplorer is designed to:

* **Explore**: Provide an intuitive way to browse a database containing scientific resources (titles, authors, journals, DOI, publication year, keywords, etc.).
* **Classify and Search**: Help users identify resources of interest through advanced filtering and sorting.
* **Interact**: Enable users to mark resources as read, add comments and ratings, or modify their information.

#### Key Features

* **User Profiles**: Create, modify, and manage user profiles with database access settings.
* **Library Search**: Filter, sort, and browse scientific resources using various criteria (title, authors, keywords, application domains, etc.).
* **Resource Management**: Add new resources to the database, update existing entries, or mark resources as read.
* **Reviews and Comments**: Leave detailed reviews or ratings for specific resources.
* **Recent Interactions**: Access the latest comments and interactions to stay updated on project progress.

## Target Audience

LitExplorer is designed for **researchers, scientists, industry professionals, and students** interested in addressing nitrosamine-related challenges in the pharmaceutical industry.

⚠️ The database entries are designed for users with a background in **chemistry** or **biology** to fully understand the content.


## Technical Requirements

1. **Programming Language**: Python (version ≥ 3.8).

2. **Dependencies**:
    * streamlit
    * pandas
    * pyodbc

3. **Virtual Environment**: Recommended for dependency isolation.

4. **Database**: A Microsoft Access database stored on a local server or synchronized via SharePoint.

Dependencies are listed in the ``requirements.txt`` file.

## Database Overview
LitExplorer relies on a Microsoft Access database to store and organize information about scientific resources. The database contains multiple tables that track resources, user interactions, and reviews.

#### Key Tables and Fields
- **Resources Table**: Stores details about the scientific resources, such as title, authors, journal, DOI, and keywords.
- **Users Table**: Contains user profiles, including login details and roles.
- **Reviews Table**: Tracks user feedback on resources, including ratings and comments.
- **Contributions Table**: Tracks user contributions like adding a new resource, modifying its details or adding a review.
- **ReadingList Table**: Manages user reading lists.

For a detailed description of the database structure, including fields and relationships, refer to the [Database Documentation](./database_structure.md).


## Installation Guide

**1. Download and Extract the Archive**
* Download the **LitExplorer.zip** file from the shared link or repository.
* Extract the archive into a directory of your choice.

**2. Set up the Application**:
* Open a terminal or command prompt and navigate to the extracted folder:

```bash
cd LitExplorer
```


* **Create and activate a virtual environment**:

```bash
python -m venv env
source env/Scripts/activate  # On Linux/Mac
.\env\Scripts\activate.bat   # On Windows
```
* **Install dependencies**:
```bash
pip install -r requirements.txt
```

**3. Configure the Database**

* **Set up the Access Database**:
    * Download and place the database on a local server or SharePoint synchronized locally.
    * Ensure all project participants have access to the database location.

**4. Launch the Application**

* **Method 1**: Activate the virtual environment and run the main script:

```bash
source env/Scripts/activate
streamlit run app.py
```

* **Method 2**: Run the `app_launcher.vbs` file directly.

## First Use

* **Launch the app** using one the methods described above.

* **Configure Database Access**:

Navigate to the **Database** page, paste the database path (copied via *Copy as Path* from the file explorer, without quotes), and click Save. The connection will be tested, and a success or error message will appear.

* **Create a User Profile**:

Go to the **Login** page, create a profile, note your login information, and sign in. Success messages will confirm each step.

#### What You Can Do Next

Once the initial setup is complete, explore the following features to fully utilize the application:

**Library**
* Browse all resources in the database.
* Filter and sort resources by title, authors, keywords, domains, and more.
* Mark resources as read, leave reviews, or rate articles directly from the library interface.
* Access detailed information for each resource.


**Reading List**
* View your personal reading list on the Readings page.
* Add articles of interest from the library to your reading list.
* Track your progress with statuses like "Not Started," "In Progress," or "Completed."
* Prioritize resources by assigning priority levels.

**Contributors and Interactions**
* View recent contributions (e.g., new resources, edited entries, reviews) on the Last Contributions page.
* Check the Last Interactions page to see the latest reviews and ratings left by other users.
* Learn about active participants and contributors to the database on the Contributors page. 

**Add or Edit Resources**
* Add new articles to the database via the New Resource page.
* Edit existing resource details to keep the database accurate and up-to-date.

**Profile Management**
* Update your profile information (e.g., username, email) on the Profile page.


## Structure and Navigation
### Structure
* **Pages** (in ``pages/``):

| **Page Name**           | **File Name**              | **Description**                                                                 |
|-------------------------|---------------------------|-------------------------------------------------------------------------------|
| **Home Page**           | `00_homepage.py`          | Introduction to the application and its features.                             |
| **Database Configuration** | `01_database.py`       | Database configuration.                                                       |
| **Login**               | `02_login.py`             | User profile management.                                                      |
| **Profile**             | `10_profile.py`           | View and edit user profiles.                                                  |
| **Readings**            | `11_readings.py`          | Veiw and interact with resources added to your reading list.                  |
| **Library**             | `20_library.py`           | Explore and interact with the database.                                       |
| **New Resource**        | `21_new_resource.py`      | Add new resources to the database.                                            |
| **Last Interactions**   | `23_last_interaction.py`  | View recent user interactions.                                                |
| **Last Contributions**  | `24_last_contributions.py`| View recent contributions such as new resources, edited resources, and reviews. |
| **Contributors**        | `25_contributors.py`      | Find out who's contributing to the project.                                   |


* **Forms** (in ``forms/``):

    * Auxiliary scripts for specific actions like adding a review, editing a resource, or view open the detailed view of a resource.

### Navigation
The application uses a sidebar for easy navigation between its core pages.

## Customization and Maintenance
* **Source Code**: All modifications (adding features, updating database fields, etc.) must be performed in the Python code.
* **Database**: Adding new fields to the database requires corresponding updates in the application scripts.

## Developer and Contributions
* **Lead Developer**: Florentin Creme
* **Contributions**:
    * Database design: Team of ECPM students with Axel Delente, Sara Sanchez and Florentin Creme,  supervised by Novartis and the school.
* **License**: No license currently applied.

## Screenshots and Tutorials
Screenshots and video tutorials on installation and basic usage will be added in future updates.

## Future Work
Here are the planned improvements and tasks for LitExplorer:

#### Features to Add
- [x] Implement filtering of contribution types.
- [x] Add a directory of contributors, sorted by number of contributions.
- [x] Add a to-do list of articles to read, with the option of assigning them a degree of importance.
- [x] Add a portfolio of articles already read.
- [ ] Add the possibility of personal notes on articles.

#### Fixes Needed
- [x] Fix bug in the "Mark as Read" functionality on the library page.
- [x] Fix bug in the display of the date on the Contributions page.

#### Improvements
- [ ] Add tips for filling in fields.
- [x] Verify that an article is not already in the database before adding it.
- [ ] Autocompletion of some fields during the creation of a new resource.
