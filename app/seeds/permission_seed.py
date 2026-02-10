from app.models import Permission

def seed_permissions():
    permissions_data = [
        # User Permissions
        {'name': 'all_users', 'display_name': 'All Users', 'group': 'Users', 'sort': 1},
        {'name': 'view_users', 'display_name': 'View Users', 'group': 'Users', 'sort': 2},
        {'name': 'add_users', 'display_name': 'Create Users', 'group': 'Users', 'sort': 3},
        {'name': 'edit_users', 'display_name': 'Edit Users', 'group': 'Users', 'sort': 4},
        {'name': 'delete_users', 'display_name': 'Delete Users', 'group': 'Users', 'sort': 5},

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

        # Category Management Permissions
        {'name': 'all_categories', 'display_name': 'All Categories', 'group': 'Categories', 'sort': 1},
        {'name': 'view_categories', 'display_name': 'View Categories', 'group': 'Categories', 'sort': 2},
        {'name': 'create_categories', 'display_name': 'Create Categories', 'group': 'Categories', 'sort': 3},
        {'name': 'edit_categories', 'display_name': 'Edit Categories', 'group': 'Categories', 'sort': 4},
        {'name': 'delete_categories', 'display_name': 'Delete Categories', 'group': 'Categories', 'sort': 5},

        # Event Management Permissions
        {'name': 'all_events', 'display_name': 'All Events', 'group': 'Events', 'sort': 1},
        {'name': 'view_events', 'display_name': 'View Events', 'group': 'Events', 'sort': 2},
        {'name': 'create_events', 'display_name': 'Create Events', 'group': 'Events', 'sort': 3},
        {'name': 'edit_events', 'display_name': 'Edit Events', 'group': 'Events', 'sort': 4},
        {'name': 'delete_events', 'display_name': 'Delete Events', 'group': 'Events', 'sort': 5},

        # Ticket Management Permissions
        {'name': 'all_tickets', 'display_name': 'All Tickets', 'group': 'Tickets', 'sort': 1},
        {'name': 'view_tickets', 'display_name': 'View Tickets', 'group': 'Tickets', 'sort': 2},
        {'name': 'create_tickets', 'display_name': 'Create Tickets', 'group': 'Tickets', 'sort': 3},
        {'name': 'edit_tickets', 'display_name': 'Edit Tickets', 'group': 'Tickets', 'sort': 4},
        {'name': 'delete_tickets', 'display_name': 'Delete Tickets', 'group': 'Tickets', 'sort': 5},

        # Booking Management Permissions
        {'name': 'all_bookings', 'display_name': 'All Bookings', 'group': 'Bookings', 'sort': 1},
        {'name': 'view_bookings', 'display_name': 'View Bookings', 'group': 'Bookings', 'sort': 2},
        {'name': 'create_bookings', 'display_name': 'Create Bookings', 'group': 'Bookings', 'sort': 3},
        {'name': 'edit_bookings', 'display_name': 'Edit Bookings', 'group': 'Bookings', 'sort': 4},
        {'name': 'delete_bookings', 'display_name': 'Delete Bookings', 'group': 'Bookings', 'sort': 5},

        # Payment Management Permissions
        {'name': 'all_payments', 'display_name': 'All Payments', 'group': 'Payments', 'sort': 1},
        {'name': 'view_payments', 'display_name': 'View Payments', 'group': 'Payments', 'sort': 2},
        {'name': 'create_payments', 'display_name': 'Create Payments', 'group': 'Payments', 'sort': 3},
        {'name': 'edit_payments', 'display_name': 'Edit Payments', 'group': 'Payments', 'sort': 4},
        {'name': 'delete_payments', 'display_name': 'Delete Payments', 'group': 'Payments', 'sort': 5},

        # Invoice Management Permissions
        {'name': 'all_invoices', 'display_name': 'All Invoices', 'group': 'Invoices', 'sort': 1},
        {'name': 'view_invoices', 'display_name': 'View Invoices', 'group': 'Invoices', 'sort': 2},
        {'name': 'create_invoices', 'display_name': 'Create Invoices', 'group': 'Invoices', 'sort': 3},
        {'name': 'edit_invoices', 'display_name': 'Edit Invoices', 'group': 'Invoices', 'sort': 4},
        {'name': 'delete_invoices', 'display_name': 'Delete Invoices', 'group': 'Invoices', 'sort': 5},

        # Checkin Management Permissions
        {'name': 'all_checkins', 'display_name': 'All Checkins', 'group': 'Checkins', 'sort': 1},
        {'name': 'view_checkins', 'display_name': 'View Checkins', 'group': 'Checkins', 'sort': 2},
        {'name': 'create_checkins', 'display_name': 'Create Checkins', 'group': 'Checkins', 'sort': 3},
        {'name': 'edit_checkins', 'display_name': 'Edit Checkins', 'group': 'Checkins', 'sort': 4},
        {'name': 'delete_checkins', 'display_name': 'Delete Checkins', 'group': 'Checkins', 'sort': 5},

        # Event Registration Permissions
        {'name': 'all_event_registrations', 'display_name': 'All Event Registrations', 'group': 'Event Registrations', 'sort': 1},
        {'name': 'view_event_registrations', 'display_name': 'View Event Registrations', 'group': 'Event Registrations', 'sort': 2},
        {'name': 'create_event_registrations', 'display_name': 'Create Event Registrations', 'group': 'Event Registrations', 'sort': 3},
        {'name': 'edit_event_registrations', 'display_name': 'Edit Event Registrations', 'group': 'Event Registrations', 'sort': 4},
        {'name': 'delete_event_registrations', 'display_name': 'Delete Event Registrations', 'group': 'Event Registrations', 'sort': 5},

        # User Profile Permissions
        {'name': 'all_user_profiles', 'display_name': 'All User Profiles', 'group': 'User Profiles', 'sort': 1},
        {'name': 'view_user_profiles', 'display_name': 'View User Profiles', 'group': 'User Profiles', 'sort': 2},
        {'name': 'create_user_profiles', 'display_name': 'Create User Profiles', 'group': 'User Profiles', 'sort': 3},
        {'name': 'edit_user_profiles', 'display_name': 'Edit User Profiles', 'group': 'User Profiles', 'sort': 4},
        {'name': 'delete_user_profiles', 'display_name': 'Delete User Profiles', 'group': 'User Profiles', 'sort': 5},
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
