from app.models import User, Role
import os

def seed_users():
    # Get the Admin role
    try:
        admin_role = Role.objects.get(name='Admin')
    except Role.DoesNotExist:
        print("Admin role does not exist. Please run role_seed.py first.")
        return

    # Create a default superuser
    admin_email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin123@gmail.com')
    admin_password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')

    if not User.objects.filter(email=admin_email).exists():
        print(f"Creating superuser '{admin_email}'...")
        user = User.objects.create_superuser(
            email=admin_email,
            password=admin_password
        )
        user.role = admin_role
        user.save()
        print(f"Superuser '{admin_email}' created with email '{admin_email}' and assigned 'Admin' role.")
    else:
        print(f"Superuser '{admin_email}' already exists.")
        # Ensure existing admin user has the admin role
        user = User.objects.get(email=admin_email)
        if user.role != admin_role:
            user.role = admin_role
            user.save()
            print(f"Existing superuser '{admin_email}' assigned 'Admin' role.")
        else:
            print(f"Existing superuser '{admin_email}' already has 'Admin' role.")

    # Create a default simple user for testing
    simple_user_email = 'simpleuser@example.com'
    simple_user_password = 'simpleuser123'

    try:
        user_role = Role.objects.get(name='User')
    except Role.DoesNotExist:
        print("User role does not exist. Please run role_seed.py first.")
        return

    if not User.objects.filter(email=simple_user_email).exists():
        print(f"Creating simple user '{simple_user_email}'...")
        user = User.objects.create_user(
            email=simple_user_email,
            password=simple_user_password
        )
        user.role = user_role
        user.save()
        print(f"Simple user '{simple_user_email}' created with email '{simple_user_email}' and assigned 'User' role.")
    else:
        print(f"Simple user '{simple_user_email}' already exists.")
        # Ensure existing simple user has the user role
        user = User.objects.get(email=simple_user_email)
        if user.role != user_role:
            user.role = user_role
            user.save()
            print(f"Existing simple user '{simple_user_email}' assigned 'User' role.")
        else:
            print(f"Existing simple user '{simple_user_email}' already has 'User' role.")



if __name__ == '__main__':
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    django.setup()
    seed_users()
