from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.synchronous.database import Database
from pymongo.synchronous.collection import Collection
from pymongo.cursor import Cursor
from pymongo.results import DeleteResult, UpdateResult

from datetime import datetime, timedelta
from backend.state_machine.database.validation import IOError, pattern_birthday


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

    def add_user(
            self, username: str, email: str, phone: str, birthday: str
        ) -> str:
        try:
            self.__coll_users.insert_one(
                document={
                    'username': username,
                    'email': email,
                    'phone': phone,
                    'birthday': datetime.strptime(birthday, pattern_birthday),
                    'notes': []
                }
            )
        except:
            raise IOError(
                f'User {username} is already present in the database. \n\n'
            )

        return f'User {username} successfully added to the database. \n\n'

    def remove_user(self, username: str) -> str:
        result: DeleteResult = self.__coll_users.delete_one(
            filter={'username': username}
        )

        if result.deleted_count == 1:
            return (
                f'User {username} '
                'successfully removed from the database. \n\n'
            )
            
        raise IOError(
            f'User {username} is not present in the database. \n\n'
        )

    def add_note(self, username: str, title: str, content: str) -> str:
        result: UpdateResult = self.__coll_users.update_one(
            filter={'username': username},
            update={
                '$addToSet': {
                    'notes': {'title': title, 'content': content}
                }
            }
        )

        if result.modified_count == 1:
            return (
                'Note with provided title '
                'successfully added to the database. \n\n'
            )
        
        raise IOError(
            'At least one of the provided data items '
            'does not satisfy requirements. \n\n'
        )

    def remove_note(self, username: str, title: str) -> str:
        result: UpdateResult = self.__coll_users.update_one(
            filter={
                'username': username,
                'notes': {'$elemMatch': {'title': title}}
            },
            update={'$unset': {'notes.$': ''}}
        )

        if result.matched_count == 1:
            return (
                'Note with provided title '
                'successfully removed from the database. \n\n'
            )

        raise IOError(
            'At least one of provided data items '
            'does not satisfy requirements. \n\n'
        )

    def show_user(self, username: str) -> str:
        user: dict = self.__coll_users.find_one(
            filter={'username': username}
        )

        if user is None:
            raise IOError(f'User {username} is absent in the database. \n\n')

        report: str = f'User {username} found in database. Profile: \n\n'

        username: str = user['username']
        email: str = user['email']
        phone: str = user['phone']
        birthday: datetime = user['birthday']

        report += (
            f'1. Username: {username} \n\n'
            f'2. Email: {email} \n\n'
            f'3. Phone: {phone} \n\n'
            f'4. Birthday: {birthday.strftime(format=pattern_birthday)} \n\n'
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
            raise IOError(f'User {username} is absent in the database. \n\n')
        
        notes: list[dict] = user.get('notes', [])

        if len(notes) == 0:
            raise IOError(f'User {username} has no notes yet. \n\n')
        
        if notes[0] is None:
            raise (f'All notes of user {username} were removed. \n\n')

        report: str = (
            f'User {username} is the authour of the following notes. \n\n'
        )

        for i, note in enumerate(notes):
            if note is not None:
                report += f'{i + 1}. Title: {note['title']} \n\n'
                report += f'- Content: {note['content']} \n\n'

        return report

    def show_birthdays(self, num_days_ahead: int) -> str:
        start: datetime = datetime.now()
        end: datetime = start + timedelta(days=num_days_ahead)

        cursor: Cursor = self.__coll_users.aggregate(
            pipeline=[
                {
                   '$project': {
                        'username': '$username',
                        'birthday': '$birthday',
                        'birthday_this_year': {
                            '$dateFromParts': {
                                'year' : start.year,
                                'month' : {'$month': '$birthday'},
                                'day': {'$dayOfMonth': '$birthday'}
                            }
                        }
                    }
                },
                {
                    '$match': {
                        '$and': [
                            {'birthday_this_year': {'$gte': start}},
                            {'birthday_this_year': {'$lte': end}}
                        ]
                    } 
                }
            ]
        )

        documents: list[dict] = list(cursor)
        num_documents: int = len(documents)
        
        report: str = (
            f'Total number of upcoming birthday celebrations in the period '
            f'from {start.strftime(format=pattern_birthday)} '
            f'to {end.strftime(format=pattern_birthday)} '
            f'is {num_documents}. \n\n'
        )

        for doc in documents:
            username: str = doc['username']
            birthday: datetime = doc['birthday']
            
            report += (
                f'- User {username}, '
                f'birthday {birthday.strftime(format=pattern_birthday)} \n\n'
            )
        
        return report

    def show_database(self, num_recent_records: int) -> str:
        cursor: Cursor = (
            self.__coll_users
            .find({})
            .sort(key_or_list='_id', direction=ASCENDING)
        )

        documents: list[dict] = list(cursor)
        num_documents: int = len(documents)

        report: str = (
            f'Total number of users in database is {num_documents}. \n\n'
        )

        if num_documents > 0:
            report += 'Recently added users are: '

            for i, doc in enumerate(documents):
                if i >= num_recent_records:
                    break

                report += f'{doc['username']}'
                
                if i < num_documents - 1:
                    report += ', '

        report += ' \n\n'
        return report


database_manager: DatabaseManager = DatabaseManager()