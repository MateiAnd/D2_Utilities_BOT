import aiosqlite
import asyncio

#  ["Cuddlie#7613", 210357426732400641]

async def session_beginner(part_list):
    async with aiosqlite.connect('./evidenta_populatiei/user_role.db') as connection:
        cursor = await connection.cursor()

        for user_id in part_list:
            # Prepare the query
            query = f'SELECT KF, DSC, GOS, LW, VOG, VOD, RON FROM UserRoles WHERE user_id = {user_id[1]}'

            # Execute the query
            await cursor.execute(query)

            # Fetch the result
            result = await cursor.fetchone()

            # If a result is found, store it in the dictionary
            for status in result:
                if not bool(status):
                    return False
            return True


async def test():
    _test = await session_beginner([["Cuddlie#7613", 210357426732400641]])
    print(_test)

asyncio.run(test())