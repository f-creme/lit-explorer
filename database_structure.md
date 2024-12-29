# Database Structure for LitExplorer

## Introduction

This document provides an overview of the Microsoft Access database structure used in **LitExplorer**. The database is designed to organize and manage scientific literature on nitrosamines, enabling efficient storage, retrieval, and interaction with the data.

The database consists of several tables, each with a specific role in supporting the application’s functionality. Key tables include:
- **Resources**: Stores metadata about scientific articles.
- **Users**: Tracks user profiles and roles.
- **Reviews**: Records user feedback on resources.
- **Contributions**: Logs user interactions with the database.

---

## Tables Overview

#### 1. **Resources**
This table stores detailed information about each scientific resource in the library.

| Field Name            | Type           | Description                                  |
|-----------------------|----------------|----------------------------------------------|
| `ResourceID`          | Integer (Auto) | Unique identifier for the resource.         |
| `Title`               | Text           | Title of the scientific article.            |
| `Authors`             | Long Text      | List of authors for the resource.           |
| `Journal`             | Text           | Name of the journal where the article was published. |
| `Date`                | Integer        | Year of publication.                        |
| `DOI`                 | Text           | Digital Object Identifier of the article.   |
| `Document Type`       | Text           | Type of document (e.g., article, report).   |
| `Article Type`        | Text           | Classification of the article (e.g., review, primary research). |
| `Application Field`   | Text           | Application domain (e.g., pharmaceuticals). |
| `Category`            | Text           | General category of the resource.           |
| `Sub Category`        | Text           | Specific category for finer classification.  |
| `Specific to Nitrosamines` | Text      | Indicates if the resource focuses on nitrosamines. |
| `Keywords`            | Long Text      | Keywords associated with the resource, separated by ", ".      |
| `Rating`              | Double         | Average rating calculated from user reviews.           |
| `Summary`             | Long Text      | A brief summary of the article.             |
| `Reader`              | Long Text      | List of UserLogin of users who have read the resource.            |

---

#### 2. **Users**
This table tracks user profiles and their roles in the application.

| Field Name         | Type           | Description                                  |
|--------------------|----------------|----------------------------------------------|
| `UserID`           | Integer (Auto) | Unique identifier for each user.            |
| `Username`         | Text           | Display name of the user.                   |
| `UserLogin`        | Text           | User’s login credential.                    |
| `UserRegDate`      | Date/Time      | Registration date of the user.              |
| `UserRole`         | Text           | Role of the user.                           |
| `UserDesc`         | Long Text      | Additional description or profile details.  |
| `UserMail`         | Text           | Contact email of the user.                  |
| `UserContributions`| Integer        | Number of contributions made by the user.   |
| `UserPicURL`       | Long Text      | URL to the user’s profile picture.          |

---

#### 3. **Reviews**
Stores user feedback on resources, including ratings and detailed reviews.

| Field Name      | Type           | Description                                  |
|-----------------|----------------|----------------------------------------------|
| `ReviewID`      | Integer (Auto) | Unique identifier for each review.           |
| `ContributionID`| Integer        | ID linking the review to a specific contribution. |
| `ResourceID`    | Integer        | ID of the resource being reviewed.           |
| `UserLogin`     | Text           | Login of the user who wrote the review.      |
| `ReviewDate`    | Date/Time      | Date when the review was submitted.          |
| `Review`        | Long Text      | Detailed feedback or comment.                |
| `Rating`        | Integer        | User’s rating for the resource (e.g., 1–5). |

---

#### 4. **Contributions**
Logs interactions between users and resources, such as edits or comments.

| Field Name         | Type           | Description                                  |
|--------------------|----------------|----------------------------------------------|
| `ContributionID`   | Integer (Auto) | Unique identifier for each contribution.    |
| `ContributionDate` | Date/Time      | Date when the contribution was made.        |
| `ContributionType` | Text           | Type of contribution (e.g., "New Resource", "New Review"). |
| `ResourceID`       | Integer        | ID of the resource associated with the contribution. |
| `UserLogin`        | Text           | Login of the contributing user.             |

---

### 5. **ReadingList**
This table tracks articles that users add to their personal reading lists, including priority levels and progress status.

| Column Name      | Type           | Description                                   |
|------------------|----------------|-----------------------------------------------|
| `ReadingListID`  | Auto-Increment | Unique identifier for each entry in the reading list. |
| `UserLogin`         | Foreign Key    | Reference to the user in the `Users` table.   |
| `ResourceID`     | Foreign Key    | Reference to the article in the `Resources` table. |
| `Priority`       | Integer        | Priority level (1 = High, 2 = Medium, 3 = Low). |
| `DateAdded`      | DateTime       | Date and time the article was added to the reading list. |
| `Status`         | Integer           | Status of the article (1="Not Started", 2="In Progress", 3="Completed"). |


## Relationships

- **Resources** and **Reviews**: Linked by `ResourceID` to associate reviews with specific resources.
- **Users** and **Reviews**: Connected via `UserLogin` to track user feedback.
- **Users** and **Contributions**: Linked by `UserLogin` to log user actions.
- **Resources** and **Contributions**: Connected by `ResourceID` to log edits or interactions.
- **ReadingList** and **Users**: Linked by `UserLogin`.
- **ReadingList** and **Resources**: Linked by `ResourceID`.

---

