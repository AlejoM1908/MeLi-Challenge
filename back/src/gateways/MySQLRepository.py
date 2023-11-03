import mysql.connector.pooling
from src.entities.Repositories import Repository, Classification
from src.entities.User import User
from src.entities.Role import Role
from src.entities.Risk import Risk
from src.entities.Provider import Provider
from typing import Union
import bcrypt

class HashingError(Exception):
    pass

class MySQLRepository(Repository):
    def __init__(self, config):
        self._pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="mysql-pool",
                                                                pool_size=5,
                                                                **config)
        
    def _hashPassword(self, clear_text: str, *, salt:any = None, salt_difficulty: int = 12) -> tuple[str,str]:
        """
        Takes a clear text password and returns a tuple with the hashed password and the salt used to hash it with bcrypt

        Positional arguments:
            clear_text {str} -- The password to hash

        Keyword arguments:
            salt {any} -- The salt to use to hash the password. Default is None
            salt_difficulty {int} -- The difficulty level to use to hash the password (2**salt_difficulty iterations). Default is 12

        Returns:
            tuple[str,str] -- A tuple with the hashed password and the salt used to hash it

        Raises:
            HashingError -- If the password is empty or if an error ocurred while hashing the password
        """
        if not clear_text:
            raise HashingError('Password cannot be empty')
        
        try:
            # Use bcrypt to hash the password
            salt = bcrypt.gensalt(salt_difficulty) if not salt else salt
            return (bcrypt.hashpw(clear_text.encode('utf-8'), salt), salt)
        except Exception as e:
            raise HashingError(e.args[0])
    
    def _checkPassword(self, plain_Text: str, stored_hash: str) -> bool:
        """
        Takes a plain text password and the stored hash and returns True if the password matches the hash.
        Remember that the salt is stored in the hash itself, so no need to provide it.

        Arguments:
            plain_Text {str} -- The plain text password to check
            stored_hash {str} -- The stored hash to compare with

        Returns:
            bool -- True if the password matches the hash

        Raises:
            HashingError -- If the password or the hash are empty or if an error ocurred while hashing the password
        """
        if not plain_Text or not stored_hash:
            raise HashingError('Provided hashes cannot be empty')
        
        try:
            # Compare the hashes
            return bcrypt.checkpw(plain_Text.encode('utf-8'), stored_hash.encode('utf-8'))
        except Exception as e:
            raise HashingError(e.args[0])
        
    def _queryDB(self, query: str, params: tuple = None, *, error_message:str = None, fetch_all: bool = False, fetch_one: bool = False, get_last_id:bool = False) -> Union[bool,int,str,list[tuple],tuple]:
        """
        Executes a query in the database and returns the result, properly managing the connection pool
        
        Positional arguments:
            query {str} -- The query to execute
            params {tuple} -- The parameters to pass to the query. Default is None

        Keyword arguments:
            error_message {str} -- The error message to return if the query fails. Default is 'An error ocurred while executing the query in the database'
            fetch_all {bool} -- If the query should return a list of tuples. Default is False
            fetch_one {bool} -- If the query should return a tuple. Default is False
            get_last_id {bool} -- If the query should return the last inserted id. Default is False

        Returns:
            String -- The error message if the query fails
            Boolean -- True if the query was executed successfully
            List[tuple] -- The result of the query if fetch_all is True
            tuple -- The result of the query if fetch_one is True
        """
        if not query:
            return 'It is required to provide a query to execute'

        if not error_message:
            error_message = 'An error ocurred while executing the query in the database'

        connection = self._pool.get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(query, params)
            if fetch_all:
                return cursor.fetchall()
            elif fetch_one:
                return cursor.fetchone()
            elif get_last_id:
                connection.commit()
                return cursor.lastrowid
            else:
                connection.commit()
                return True
        except Exception as e:
            return error_message
        finally:
            connection.close()
    
    def createUser(self, email: str, password: str, name: str) -> Union[int,str]:
        if not email or not password or not name:
            return 'Any of the required fields is empty, please fill all the fields'
        
        query = 'INSERT INTO `user` (`email`, `hash`, `salt`, `name`) VALUES (%s, %s, %s, %s)'
        try:
            hashed_password, salt = self._hashPassword(password)
            
            return self._queryDB(query, (email, hashed_password, salt, name), get_last_id=True, error_message='Error creating user')
        except HashingError as e:
            return 'An error ocurred while hashing the password'

    def getUserById(self, id: int) -> Union[User,str]:
        query = 'SELECT `id`, `email`, `hash`, `salt`, `name`, `created_at`, `updated_at` FROM `user` WHERE `id` = %s'

        result =self._queryDB(query, (id,), fetch_one=True, error_message='Error obtaining user')
        
        return User(*result)

    def getUserByEmail(self, email: str) -> Union[User,str]:
        query = 'SELECT `id`, `email`, `hash`, `salt`, `name`, `created_at`, `updated_at` FROM `user` WHERE `email` = %s'

        result = self._queryDB(query, (email,), fetch_one=True)
        
        return result if isinstance(result, Union[str,None]) else User(*result)
    
    def getUserWithRoles(self, id: int) -> Union[User,str]:
        query = 'SELECT q.`id`,q.`email`,q.`hash`,q.`salt`,q.`name`,q.`created_at`,q.`updated_at`,q.`role_name` FROM (SELECT`user`.`id`,`email`,`hash`,`salt`,`user`.`name`,`user`.`created_at`,`user`.`updated_at`,`role`.`name` as "role_name" FROM `user`INNER JOIN `user_role` ON `user`.`id` = `user_role`.`user_id`INNER JOIN `role` ON `user_role`.`role_id` = `role`.`id`WHERE `user`.`id` = %s) AS q'

        results = self._queryDB(query, (id,), fetch_all=True, error_message='Error obtaining user')

        if not isinstance(results, list):
            return results
        
        user = User(*results[0][:-1])
        user.roles = [result[-1] for result in results]

        return user
    
    def getRiskWithUsers(self, id: int) -> Union[Risk,str]:
        query = 'SELECT q.`id`,q.`provider_id`,q.`name`,q.`description`,q.`probability`,q.`impact`,q.`created_at`,q.`updated_at`,q.`user_id` FROM (SELECT `risk`.`id`,`provider_id`,`name`,`description`,`probability`,`impact`,`risk`.`created_at`,`risk`.`updated_at`,`user`.`id` as "user_id" FROM `risk`INNER JOIN `risk_user` ON `risk`.`id` = `risk_user`.`risk_id`INNER JOIN `user` ON `risk_user`.`user_id` = `user`.`id`WHERE `risk`.`id` = %s) AS q'

        results = self._queryDB(query, (id,), fetch_all=True, error_message='Error obtaining risk')

        if not isinstance(results, list):
            return results
        
        risk = Risk(*results[0][:-1])
        risk.user_ids = [result[-1:] for result in results]

        return risk

    def getUsersByRole(self, role: str) -> Union[list[User],str]:
        query = 'SELECT q.`id`, q.`email`, q.`hash`, q.`salt`, q.`name`, q.`created_at`, q.`updated_at`, q.`role_id` FROM (SELECT `id`, `email`, `hash`, `salt`, `name`, `created_at`, `updated_at`, `role_id` FROM `user`  INNER JOIN `user_role` ON `user`.`id` = `user_role`.`user_id` INNER JOIN `role` ON `user_role`.`role_id` = `role`.`id` WHERE `role`.`name` = %s) AS q'

        results = self._queryDB(query, (role,), fetch_all=True, error_message='Error obtaining users')
        
        return results if isinstance(results, str) else [User(*result) for result in results]

    def getAllUsers(self) -> Union[list[User],str]:
        query = 'SELECT `id`, `email`, `hash`, `salt`, `name`, `created_at`, `updated_at` FROM `user`'

        results = self._queryDB(query, fetch_all=True, error_message='Error obtaining users')
        
        return results if isinstance(results, str) else [User(*result) for result in results]

    def updateUserData(self, user: User) -> Union[bool,str]:
        if not user:
            return 'It is required to provide a user to update'

        query = 'UPDATE `user` SET `email` = %s, `name` = %s WHERE `id` = %s'

        return self._queryDB(query, (user.email, user.name, user.id), error_message='Error updating user')

    def updateUserPassword(self, user:User) -> Union[bool,str]:
        if not user:
            return 'It is required to provide a user to update'

        if user.password is None:
            return 'User password cannot be empty'

        query = 'UPDATE `user` SET `hash` = %s, `salt` = %s WHERE `id` = %s'

        try:
            hashed_password, salt = self._hashPassword(user.password)
            return self._queryDB(query, (hashed_password, salt, user.id), error_message='Error updating user')
        except HashingError as e:
            return 'An error ocurred while hashing the password'

    def deleteUser(self, id: int) -> Union[bool,str]:
        query = 'DELETE FROM `user` WHERE `id` = %s'

        return self._queryDB(query, (id,), error_message='Error deleting user')
        
    def validateUser(self, user:User) -> Union[bool,str]:
        if not user:
            return 'It is required to provide a user to validate'
        
        if not user.password:
            return 'User password cannot be empty'
        
        db_user = self.getUserByEmail(user.email)

        if isinstance(db_user, str):
            return 'The user cannot be validated'
        
        try:
            if not self._checkPassword(user.password, db_user.hashed_password):
                return 'The user cannot be validated'

            return True
        except HashingError:
            return 'The user cannot be validated'

    def linkRoleToUser(self, user_id: int, role_id: int) -> Union[bool,str]:
        query = 'INSERT INTO `user_role` (`user_id`, `role_id`) VALUES (%s, %s)'

        return self._queryDB(query, (user_id, role_id), error_message='Error asigning role to user')

    def unlinkRoleToUser(self, user_id: int, role_id: int) -> Union[bool,str]:
        query = 'DELETE FROM `user_role` WHERE `user_id` = %s AND `role_id` = %s'

        return self._queryDB(query, (user_id, role_id), error_message='Error removing role to user')

    def getAllRoles(self) -> Union[list[Role],str]:
        query = 'SELECT `id`, `name`, `created_at`, `updated_at` FROM `role`'

        results = self._queryDB(query, fetch_all=True, error_message='Error obtaining roles')
        
        return results if isinstance(results, str) else [Role(*result) for result in results]

    def createRole(self, name: str) -> Union[int,str]:
        query = 'INSERT INTO `role` (`name`) VALUES (%s)'

        return self._queryDB(query, (name,), get_last_id=True, error_message='Error creating rol')

    def getRoleById(self, id: int) -> Union[Role,str]:
        query = 'SELECT `id`, `name`, `created_at`, `updated_at` FROM `role` WHERE `id` = %s'

        result = self._queryDB(query, (id,), fetch_one=True, error_message='Error obtaining rol')
        
        return result if isinstance(result, Union[str,None]) else Role(*result)
    
    def getRoleByName(self, name: str) -> Union[Role,str]:
        query = 'SELECT `id`, `name`, `created_at`, `updated_at` FROM `role` WHERE `name` = %s'

        result = self._queryDB(query, (name,), fetch_one=True, error_message='Error obtaining rol')
        
        return result if isinstance(result, Union[str,None]) else Role(*result)
        
    def updateRole(self, role: Role) -> Union[bool,str]:
        if not role:
            return 'It is required to provide a role to update'

        query = 'UPDATE `role` SET `name` = %s WHERE `id` = %s'

        return self._queryDB(query, (role.name, role.id), error_message='Error updating rol')

    def deleteRole(self, id: int) -> Union[bool,str]:
        query = 'DELETE FROM `role` WHERE `id` = %s'

        return self._queryDB(query, (id,), error_message='Error deleting role')
        
    def createProvider(self, name: str, description: str, country:str) -> Union[int,str]:
        query = 'INSERT INTO `provider` (`name`, `description`, `country`) VALUES (%s, %s, %s)'

        return self._queryDB(query, (name, description, country), get_last_id=True, error_message='Error creating provider')

    def getProviderById(self, id: int) -> Union[Provider,str]:
        query = 'SELECT `id`, `name`, `description`, `created_at`, `updated_at` FROM `provider` WHERE `id` = %s'

        result = self._queryDB(query, (id,), fetch_one=True, error_message='the user couldn\'t be retrieved')
        
        return result if isinstance(result, Union[str,None]) else Provider(*result)
    
    def getProviderByName(self, name: str) -> Union[Provider,str]:
        query = 'SELECT `id`, `name`, `description`, `created_at`, `updated_at` FROM `provider` WHERE `name` = %s'

        result = self._queryDB(query, (name,), fetch_one=True, error_message='the user couldn\'t be retrieved')
        
        return result if isinstance(result, Union[str,None]) else Provider(*result)
    
    def getAllProviders(self) -> Union[list[Provider],str]:
        query = 'SELECT `id`, `name`, `description`, `country`, `created_at`, `updated_at` FROM `provider`'

        results = self._queryDB(query, fetch_all=True, error_message='the users couldn\'t be retrieved')
        
        return results if isinstance(results, str) else [Provider(*result) for result in results]
        
    def updateProvider(self, provider: Provider) -> Union[bool,str]:
        if not provider:
            return 'It is required to provide a provider to update'

        query = 'UPDATE `provider` SET `name` = %s, `description` = %s, `country`= %s WHERE `id` = %s'

        return self._queryDB(query, (provider.name, provider.description, provider.country, provider.id), error_message='Error updating provider')
        
    def deleteProvider(self, id: int) -> Union[bool,str]:
        query = 'DELETE FROM `provider` WHERE `id` = %s'

        return self._queryDB(query, (id,), error_message='Error al eliminar proveedor')

    def createRisk(self, provider_id:int, name: str, description: str, probability: Classification, impact: Classification) -> Union[int,str]:
        query = 'INSERT INTO `risk` (`provider_id`, `name`, `description`, `probability`, `impact`) VALUES (%s, %s, %s, %s, %s)'

        return self._queryDB(query, (provider_id, name, description, probability, impact), get_last_id=True, error_message='Error creating risk')

    def getRiskById(self, id: int) -> Union[Risk,str]:
        query = 'SELECT `id`, `provider_id`, `name`, `description`, `probability`, `impact`, `created_at`, `updated_at` FROM `risk` WHERE `id` = %s'

        result = self._queryDB(query, (id,), fetch_one=True, error_message='Error obtaining risk')
        
        return result if isinstance(result, Union[str,None]) else Risk(*result)

    def getRisksByString(self, string: str) -> Union[list[Risk],str]:
        query = 'SELECT `id`, `name`, `description`, `probability`, `impact`, `created_at`, `updated_at` FROM `risk` WHERE `name` LIKE %s OR `description` LIKE %s'

        results = self._queryDB(query, (f'%{string}%', f'%{string}%'), fetch_all=True, error_message='Error obtaining risks')
        
        return results if isinstance(results, str) else [Risk(*result) for result in results]

    def getRisksByProbability(self, probability: Classification) -> Union[list[Risk],str]:
        query = 'SELECT `id`, `name`, `description`, `probability`, `impact`, `created_at`, `updated_at` FROM `risk` WHERE `probability` = %s'

        results = self._queryDB(query, (probability,), fetch_all=True, error_message='Error obtaining risks')
        return results if isinstance(results, str) else [Risk(*result) for result in results]

    def getRisksByImpact(self, impact: Classification) -> Union[list[Risk],str]:
        query = 'SELECT `id`, `name`, `description`, `probability`, `impact`, `created_at`, `updated_at` FROM `risk` WHERE `impact` = %s'

        results = self._queryDB(query, (impact,), fetch_all=True, error_message='Error obtaining risks')
        
        return results if isinstance(results, str) else [Risk(*result) for result in results]

    def getRisksByUser(self, user: User) -> Union[list[Risk],str]:
        query = 'SELECT q.`id`, q.`name`, q.`description`, q.`probability`, q.`impact`, q.`created_at`, q.`updated_at` FROM (SELECT `risk`.`id`, `name`, `description`, `probability`, `impact`, `created_at`, `updated_at` FROM `risk`  INNER JOIN `risk_user` ON `risk`.`id` = `risk_user`.`risk_id` WHERE `risk_user`.`user_id` = %s) AS q'

        results = self._queryDB(query, (user.id,), fetch_all=True, error_message='Error obtaining risks')
        
        return results if isinstance(results, str) else [Risk(*result) for result in results]
        
    def getRisksByProvider(self, provider: Provider) -> Union[list[Risk],str]:
        query = 'SELECT `id`, `name`, `description`, `probability`, `impact`, `created_at`, `updated_at` FROM `risk` WHERE `provider_id` = %s'

        results = self._queryDB(query, (provider.id,), fetch_all=True, error_message='Error obtaining risks')
        
        return results if isinstance(results, str) else [Risk(*result) for result in results]
    
    def getRisksByCountry(self, country: str) -> Union[list[Risk],str]:
        query = 'SELECT q.`id`, q.`provider_id`, q.`name`, q.`description`, q.`probability`, q.`impact`, q.`created_at`, q.`updated_at`, q.`country` FROM (SELECT `risk`.`id`, `provider_id`, `risk`.`name`, `risk`.`description`, `probability`, `impact`, `risk`.`created_at`, `risk`.`updated_at`, `provider`.`country` FROM `risk`  INNER JOIN `provider` ON `risk`.`provider_id` = `provider`.`id` WHERE `provider`.`country` = %s) AS q'

        results = self._queryDB(query, (country,), fetch_all=True, error_message='Error obtaining risks')

        return results if isinstance(results, str) else [Risk(*result) for result in results]
    
    def getAllRisks(self) -> Union[list[Risk],str]:
        query = 'SELECT `id`, `provider_id`, `name`, `description`, `probability`, `impact`, `created_at`, `updated_at` FROM `risk`'

        results = self._queryDB(query, fetch_all=True, error_message='Error obtaining risks')
        
        return results if isinstance(results, str) else [Risk(*result) for result in results]

    def getAllRisksWithUser(self) -> Union[list[Risk],str]:
        query = 'SELECT q.`id`, q.`provider_id`, q.`name`, q.`description`, q.`probability`, q.`impact`, q.`created_at`, q.`updated_at`, q.`user_id` FROM (SELECT `id`, `provider_id`, `name`, `description`, `probability`, `impact`, `created_at`, `updated_at`, `user_id` FROM `risk`  INNER JOIN `risk_user` ON `risk`.`id` = `risk_user`.`risk_id`) AS q'

        results = self._queryDB(query, fetch_all=True, error_message='Error obtaining risks')
        
        return results if isinstance(results, str) else [Risk(*result) for result in results]

    def updateRisk(self, risk: Risk) -> Union[bool,str]:
        if not Risk:
            return 'It is required to provide a risk to update'

        query = 'UPDATE `risk` SET `name` = %s, `description` = %s, `probability` = %s, `impact` = %s, `provider_id` = %s WHERE `id` = %s'

        return self._queryDB(query, (risk.name, risk.description, risk.probability, risk.impact, risk.provider_id, risk.id), error_message='Error updating risk')

    def deleteRisk(self, id: int) -> Union[bool,str]:
        query = 'DELETE FROM `risk` WHERE `id` = %s'

        return self._queryDB(query, (id,), error_message='Error deleting risk')

    def relateRiskToUser(self, risk_id:int, user_id:int) -> Union[bool,str]:
        query = 'INSERT INTO `risk_user` (`risk_id`, `user_id`) VALUES (%s, %s)'

        return self._queryDB(query, (risk_id, user_id), error_message='Error relating risk with user')

    def unrelateRiskToUser(self, risk_id:int, user_id:int) -> Union[bool,str]:
        query = 'DELETE FROM `risk_user` WHERE `risk_id` = %s AND `user_id` = %s'

        return self._queryDB(query, (risk_id, user_id), error_message='Error unrelating risk with user')