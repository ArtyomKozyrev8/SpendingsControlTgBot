"""
First migration.
"""

from yoyo import step

__depends__ = {}

steps = (
    # CREATE Table users:

    step(
        """
            CREATE TABLE IF NOT EXISTS users(
                tg_chat_id BIGINT PRIMARY KEY UNIQUE NOT NULL,
                users_group UUID DEFAULT NULL,
                active BOOLEAN DEFAULT TRUE,
                created_dt TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
                deactivated_dt TIMESTAMP WITH TIME ZONE DEFAULT NULL
            );
        """,
        """
            DROP TABLE IF EXISTS users;
        """,
    ),
    step(
        """
            COMMENT ON COLUMN users.tg_chat_id IS 'Unique user id in the telegram group/chat.';
            COMMENT ON COLUMN users.users_group IS 'Group of users who make purchases together';
            COMMENT ON COLUMN users.active IS 'Shows if user is still active (want to use app) in the application.';
            COMMENT ON COLUMN users.created_dt IS 'Time when the user was created.';
            COMMENT ON COLUMN users.deactivated_dt IS 'Time when user was deactivated (last time).';   
        """,
    ),
    step(
        """
            CREATE INDEX IF NOT EXISTS users_active_idx ON users USING HASH (active);
        """,
        """
            DROP INDEX IF EXISTS users_active_idx;
        """,
    ),
    step(
        """
            CREATE INDEX IF NOT EXISTS users_group_idx ON users USING HASH (users_group);
        """,
        """
            DROP INDEX IF EXISTS users_group_idx;
        """,
    ),

    # CREATE Table purchase_parsing_templates:

    step(
        """
            CREATE TABLE IF NOT EXISTS purchase_parsing_templates(
                id SERIAL PRIMARY KEY,
                tg_chat_id BIGINT NOT NULL,
                template VARCHAR(255) NOT NULL,
                active BOOLEAN DEFAULT TRUE,
                created_dt TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
                deactivated_dt TIMESTAMP WITH TIME ZONE DEFAULT NULL
            );
            ALTER TABLE purchase_parsing_templates
            ADD CONSTRAINT tg_chat_id_fk
            FOREIGN KEY (tg_chat_id) REFERENCES users (tg_chat_id);
        """,
        """
            DROP TABLE IF EXISTS parsing_templates;
        """,
    ),
    step(
        """
            COMMENT ON COLUMN purchase_parsing_templates.tg_chat_id IS
             'Link to user who use the template. User can have several templates.';
            COMMENT ON COLUMN purchase_parsing_templates.template IS
             'Regular expression which is used to parse messages';
            COMMENT ON COLUMN purchase_parsing_templates.active IS 'Shows if user still use the template';
            COMMENT ON COLUMN purchase_parsing_templates.created_dt IS 'Time when the template was created.';
            COMMENT ON COLUMN purchase_parsing_templates.deactivated_dt IS 
             'Time when the template was deactivated (last time).';   
        """,
    ),
    step(
        """
            CREATE INDEX IF NOT EXISTS purchase_parsing_templates_active_idx
             ON purchase_parsing_templates USING HASH (active);
        """,
        """
            DROP INDEX IF EXISTS purchase_parsing_templates_active_idx;
        """,
    ),

    # CREATE Table purchases:

    step(
        """
            CREATE TABLE IF NOT EXISTS purchases(
                id SERIAL PRIMARY KEY,
                seller_name VARCHAR(255) NOT NULL DEFAULT 'DEFAULT_SELLER',
                purchase_type VARCHAR(255) NOT NULL DEFAULT 'DEFAULT_PURCHASE_TYPE',
                tg_chat_id BIGINT NOT NULL,
                purchase_sum BIGINT NOT NULL,
                active BOOLEAN DEFAULT TRUE,
                created_dt TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
                deactivated_dt TIMESTAMP WITH TIME ZONE DEFAULT NULL
            );
            
            ALTER TABLE purchases
            ADD CONSTRAINT tg_chat_id_fk
            FOREIGN KEY (tg_chat_id) REFERENCES users (tg_chat_id);
        """,
        """
            DROP TABLE IF EXISTS purchases;
        """,
    ),
    step(
        """
            COMMENT ON COLUMN purchases.seller_name IS 'The seller name (e.g. Wallmart or McDonalds).';
            COMMENT ON COLUMN purchases.purchase_type IS 'The purchase type (e.g. train tickets or grocery).';
            COMMENT ON COLUMN purchases.tg_chat_id IS 'Link to user who made the purchase.';
            COMMENT ON COLUMN purchases.purchase_sum IS 'Sum of the purchase. Money is in minor units (e.g. cents).';
            COMMENT ON COLUMN purchases.active IS 'Shows if purchase was cancelled.';
            COMMENT ON COLUMN purchases.created_dt IS 'Time when the purchase was created.';
            COMMENT ON COLUMN purchases.deactivated_dt IS 'Time when the purchase was deactivated.';
        """,
    ),
    step(
        """
            CREATE INDEX IF NOT EXISTS purchases_seller_name_idx
             ON purchases USING HASH (seller_name);
        """,
        """
            DROP INDEX IF EXISTS purchases_seller_name_idx;
        """,
    ),
    step(
        """
            CREATE INDEX IF NOT EXISTS purchases_purchase_type_idx
             ON purchases USING HASH (purchase_type);
        """,
        """
            DROP INDEX IF EXISTS purchases_purchase_type_idx;
        """,
    ),
)
