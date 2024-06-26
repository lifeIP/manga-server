
def deploy():
	"""Run deployment tasks."""
	from app import create_app,db
	from flask_migrate import upgrade,migrate,init,stamp
	from src.database.models import User, UserSettings, SiteSettings, Project, ProjectSettings, PreviewImage

	app = create_app()
	app.app_context().push()
	db.create_all()

	# migrate database to latest revision
	init(directory="src/database/migration")
	stamp(directory="src/database/migration")
	migrate(directory="src/database/migration")
	upgrade(directory="src/database/migration")

	