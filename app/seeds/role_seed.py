from app.models import Role, Permission, RolePermission

def seed_roles():
    # Step 1: Get all available permissions from the database
    all_permissions = Permission.objects.all()

    # Step 2: Define roles and which permissions each role should have
    roles_to_create = [
        {
            'role_name': 'Admin',
            'role_display_name': 'Administrator',
            'assigned_permissions': all_permissions  # Admin gets all permissions
        },
        {
            'role_name': 'User',
            'role_display_name': 'Regular User',
            'assigned_permissions': [
                Permission.objects.get(name='view_users'),  # User can only view users
            ]
        },
    ]

    # Step 3: Loop through each role and create it if it doesn't exist
    for role_info in roles_to_create:
        role, created = Role.objects.get_or_create(
            name=role_info['role_name'],
            defaults={'display_name': role_info['role_display_name']}
        )
        if created:
            print(f"Created role: {role.name}")
        else:
            print(f"Role already exists: {role.name}")

        # Step 4: Assign each permission to the role
        for permission in role_info['assigned_permissions']:
            role_perm, perm_created = RolePermission.objects.get_or_create(
                role=role,
                permission=permission
            )
            if perm_created:
                print(f"Assigned permission '{permission.name}' to role '{role.name}'")
            else:
                print(f"Permission '{permission.name}' already assigned to role '{role.name}'")


# Step 5: Setup Django environment and run the seeder
if __name__ == '__main__':
    import os
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    django.setup()
    seed_roles()
