import asyncio

from autinfo import AutInfoAsync, AutInfoSync

username, password = "9913004", "0820494501"


async def main_async():
    async with AutInfoAsync(username, password) as client:
        student_data = await client.get(9913004)
        print("Student Data:", student_data)

        student_ids = await client.get_range(9813004, 9813006)
        print("Student IDs in range:", student_ids)


def main_sync():
    client = AutInfoSync(username, password)
    student_data_sync = client.get(9913004)
    print("[Sync] Student Data:", student_data_sync)

    student_ids_sync = client.get_range(40013004, 40013006)
    print("[Sync] Student IDs in range:", student_ids_sync)


if __name__ == "__main__":
    asyncio.run(main_async())
    main_sync()
