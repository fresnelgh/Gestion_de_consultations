# init/seed_users.py

from models.model_utilisateurs import get_user_by_email, add_user

def create_default_users():
    # Utilisateurs par défaut
    utilisateurs = [
        {
            "nom": "kenne fresnel",
            "email": "fresnelktf@gmail.com",
            "mot_de_passe": "fresnel",
            "role": "admin"
        },
        {
            "nom": "fresnel1",
            "email": "fresnelktf1@gmail.com",
            "mot_de_passe": "chef123",
            "role": "chef_infirmier"
        }
    ]

    for u in utilisateurs:
        if not get_user_by_email(u["email"]):
            success = add_user(u["nom"], u["email"], u["mot_de_passe"], u["role"])
            if success:
                print(f"{u['role'].capitalize()} ajouté : {u['email']}")
            else:
                print(f"❌ Erreur lors de l'ajout de {u['email']}")
        else:
            print(f"✔️ Utilisateur déjà existant : {u['email']}")

# Exécution directe
if __name__ == "__main__":
    create_default_users()
