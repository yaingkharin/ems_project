from app.models import Permission

def seed_permissions():
    permissions_data = [
        # User Permissions
        {'name': 'all_users', 'display_name': 'All Users', 'group': 'Users', 'sort': 1},
        {'name': 'view_users', 'display_name': 'View Users', 'group': 'Users', 'sort': 2},
        {'name': 'add_users', 'display_name': 'Create Users', 'group': 'Users', 'sort': 3},
        {'name': 'edit_users', 'display_name': 'Edit Users', 'group': 'Users', 'sort': 4},
        {'name': 'delete_users', 'display_name': 'Delete Users', 'group': 'Usesr', 'sort': 5},

        # Role Permissions
        {'name': 'all_roles', 'display_name': 'All Roles', 'group': 'Roles', 'sort': 1},
        {'name': 'view_roles', 'display_name': 'View Roles', 'group': 'Roles', 'sort': 2},
        {'name': 'create_roles', 'display_name': 'Create Roles', 'group': 'Roles', 'sort': 3},
        {'name': 'edit_roles', 'display_name': 'Edit Roles', 'group': 'Roles', 'sort': 4},
        {'name': 'delete_roles', 'display_name': 'Delete Roles', 'group': 'Roles', 'sort': 5},

        # Permission Management Permissions
        {'name': 'all_permissions', 'display_name': 'All Permissions', 'group': 'Permission', 'sort': 1},
        {'name': 'view_permissions', 'display_name': 'View Permissions', 'group': 'Permission', 'sort': 2},
        {'name': 'create_permissions', 'display_name': 'Create Permissions', 'group': 'Permission', 'sort': 3},
        {'name': 'edit_permissions', 'display_name': 'Edit Permissions', 'group': 'Permission', 'sort': 4},
        {'name': 'delete_permissions', 'display_name': 'Delete Permissions', 'group': 'Permission', 'sort': 5},
        
        # Role-Permission Management Permissions
        {'name': 'all_role_permissions', 'display_name': 'All Role_Permissions', 'group': 'Role_Permissions', 'sort': 1},
        {'name': 'view_role_permissions', 'display_name': 'View Role_Permissions', 'group': 'Role_Permissions', 'sort': 2},
        {'name': 'create_role_permissions', 'display_name': 'Create Role_Permissions', 'group': 'Role_Permissions', 'sort': 3},
        {'name': 'edit_role_permissions', 'display_name': 'Edit Role_Permissions', 'group': 'Role_Permissions', 'sort': 4},
        {'name': 'delete_role_permissions', 'display_name': 'Delete Role_Permissions', 'group': 'Role_Permissions', 'sort': 5},
        
        # Test Management Permissions
        {'name': 'all_tests', 'display_name': 'All Tests', 'group': 'Tests', 'sort': 1},
        {'name': 'view_tests', 'display_name': 'View Tests', 'group': 'Tests', 'sort': 2},
        {'name': 'create_tests', 'display_name': 'Create Tests', 'group': 'Tests', 'sort': 3},
        {'name': 'edit_tests', 'display_name': 'Edit Tests', 'group': 'Tests', 'sort': 4},
        {'name': 'delete_tests', 'display_name': 'Delete Tests', 'group': 'Tests', 'sort': 5},
        
        # Venue Management Permissions
        {'name': 'all_venues', 'display_name': 'All Venues', 'group': 'Venues', 'sort': 1},
        {'name': 'view_venues', 'display_name': 'View Venues', 'group': 'Venues', 'sort': 2},
        {'name': 'create_venues', 'display_name': 'Create Venues', 'group': 'Venues', 'sort': 3},
        {'name': 'edit_venues', 'display_name': 'Edit Venues', 'group': 'Venues', 'sort': 4},
        {'name': 'delete_venues', 'display_name': 'Delete Venues', 'group': 'Venues', 'sort': 5},
    ]

    for perm_data in permissions_data:
        permission, created = Permission.objects.get_or_create(
            name=perm_data['name'],
            defaults={
                'display_name': perm_data['display_name'],
                'group': perm_data['group'],
                'sort': perm_data['sort']
            }
        )
        if created:
            print(f"Created permission: {permission.name}")
        else:
            print(f"Permission already exists: {permission.name}")

if __name__ == '__main__':
    # This block is for direct execution of the seed file for testing purposes.
    # In a real Django project, you'd typically call this from a management command
    # or a migration.
    import os
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    django.setup()
    seed_permissions()
