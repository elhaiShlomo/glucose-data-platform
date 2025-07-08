from etl.generate_data import generate_multiple_users
from etl.user_profiles import USER_PROFILES

if __name__ == '__main__':
    generate_multiple_users(USER_PROFILES)
