from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.synchronous.database import Database
from pymongo.synchronous.collection import Collection
from pymongo.cursor import Cursor
from pymongo.results import DeleteResult, UpdateResult


class DatabaseManager:
    def __init__(self) -> None:
        client = MongoClient(host='0.0.0.0', port=27017)
        print(client.list_database_names())

        self.__db_users: Database = client['db_users']
        self.__coll_users: Collection = self.create_collection()
        
    def create_collection(self) -> Collection:
        coll_users: Collection = self.__db_users['coll_users']
        coll_users.create_index(keys=[('username', DESCENDING)], unique = True)
        return coll_users
    
    def drop_collection(self) -> None:
        coll_users: Collection = self.__db_users['coll_users']
        coll_users.drop()

    def add_user(self, username: str, email: str, phone: str) -> str:
        try:
            self.__coll_users.insert_one(
                document={
                    'username': username,
                    'email': email,
                    'phone': phone,
                    'notes': []
                }
            )
        except:
            return f'User {username} is already present in the database. \n\n'

        return f'User {username} successfully added to the database. \n\n'

    def remove_user(self, username: str) -> str:
        result: DeleteResult = self.__coll_users.delete_one(
            filter={'username': username}
        )

        if result.deleted_count == 1:
            return f'User {username} successfully removed from the database. \n\n'
            
        return f'User {username} is not present in the database. \n\n'

    def add_note(self, username: str, title: str, content: str) -> str:
        result: UpdateResult = self.__coll_users.update_one(
            filter={'username': username},
            update={'$addToSet': {'notes': {'title': title, 'content': content}}}
        )

        if result.modified_count == 1:
            return f'Note with provided title successfully added to the database. \n\n'
        
        return f'At least one of provided data items do not satisfy requirements. \n\n'

    def remove_note(self, username: str, title: str) -> str:
        result: UpdateResult = self.__coll_users.update_one(
            filter={'username': username, 'notes': {'$elemMatch': {'title': title}}},
            update={'$unset': {'notes.$': ''}}
        )

        if result.matched_count == 1:
            return 'Note with provided title successfully removed from the database. \n\n'

        return f'At least one of provided data items do not satisfy requirements. \n\n'

    def show_user(self, username: str) -> str:
        user: dict = self.__coll_users.find_one(
            filter={'username': username}
        )

        if user is None:
            return f'User {username} is absent in the database. \n\n'

        report: str = 'User found in database. Profile: \n\n'
        
        report += (
            f'1. Username: {user['username']} \n\n'
            f'2. Email: {user['email']} \n\n'
            f'3. Phone: {user['phone']} \n\n'
        )

        report += (
            'show-notes command can be applied ' 
            'to display the notes written by the user. \n\n'
        )

        return report
    
    def show_notes(self, username: str) -> str:
        user: dict = self.__coll_users.find_one(
            filter={'username': username}
        )

        if user is None:
            return f'User {username} is absent in the database. \n\n'
        
        notes: list[dict] = user.get('notes', [])

        if len(notes) == 0:
            return f'User {username} has no notes yet. \n\n'
        
        if notes[0] is None:
            return f'All notes of user {username} were removed. \n\n'

        notes_report: str = f'User {username} is the authour of the following notes. \n\n'
        for note in notes:
            if note is not None:
                notes_report += f'Title: {note['title']} \n\n'
                notes_report += f'Content: {note['content']} \n\n'

        return notes_report

    def show_database(self, num_recent_records: int) -> str:
        cursor: Cursor = self.__coll_users.find(
            {}
        ).sort(
            key_or_list='_id', direction=ASCENDING
        )

        documents: list[dict] = list(cursor)
        num_documents: int = len(documents)

        report: str = (
            f'Total number of users in database is {num_documents}. \n\n'
        )

        if num_documents > 0:
            report += 'Usernames are: '

            for i, doc in enumerate(documents):
                if i >= num_recent_records:
                    break

                report += f'{doc['username']}'
                
                if i < num_documents - 1:
                    report += ', '
                

        report += ' \n\n'

        return report


database_manager: DatabaseManager = DatabaseManager()