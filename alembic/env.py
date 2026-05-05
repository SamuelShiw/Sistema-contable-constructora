from logging.config import fileConfig


from app.modules.companies.models import Company
from app.modules.roles.models import Role
from app.modules.roles.permissions import Permission
from app.modules.roles.role_permissions import RolePermission
from app.modules.users.models import User
from app.modules.users.user_roles import UserRole
from app.modules.accounting_periods.models import AccountingPeriod
from app.modules.customers.models import Customer
from app.modules.suppliers.models import Supplier
from app.modules.projects.models import Project
from app.modules.cost_centers.models import CostCenter
from app.modules.chart_accounts.models import ChartAccount




from alembic import context
from sqlalchemy import engine_from_config, pool

from app.core.database import Base

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section)

    if configuration is None:
        raise RuntimeError("No se pudo cargar la configuración de Alembic.")

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()