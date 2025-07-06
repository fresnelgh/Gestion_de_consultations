# controllers/navigation.py

def open_login_window():
    from views.vue_login import launch_login_window
    launch_login_window()

def open_infirmier_dashboard(user_id, nom_utilisateur, email_utilisateur):
    from views.vue_infirmier import launch_infirmier_view
    launch_infirmier_view(user_id, nom_utilisateur, email_utilisateur)
