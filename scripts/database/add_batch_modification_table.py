"""
Database migration script for adding BatchResumeModification table
批量简历修改表的数据库迁移脚本
"""

from flask import Flask
from app.extensions import db
from app.models.temp import BatchResumeModification
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_batch_modification_table(app):
    """
    Create the batch_resume_modifications table
    
    Args:
        app: Flask application instance
    """
    with app.app_context():
        try:
            # Create the table
            logger.info("Creating batch_resume_modifications table...")
            
            # Use db.create_all() to create only the new table
            # This is safe as it won't affect existing tables
            db.create_all()
            
            logger.info("✓ batch_resume_modifications table created successfully!")
            
            # Verify the table was created
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            if 'batch_resume_modifications' in tables:
                logger.info("✓ Table verification successful")
                
                # Show table columns
                columns = inspector.get_columns('batch_resume_modifications')
                logger.info(f"Table has {len(columns)} columns:")
                for col in columns:
                    logger.info(f"  - {col['name']}: {col['type']}")
                
                return True
            else:
                logger.error("✗ Table not found after creation")
                return False
                
        except Exception as e:
            logger.error(f"Error creating table: {str(e)}")
            db.session.rollback()
            return False


if __name__ == '__main__':
    from app import create_app
    
    # Create Flask app
    app = create_app()
    
    # Run migration
    logger.info("=" * 60)
    logger.info("Starting database migration for BatchResumeModification")
    logger.info("=" * 60)
    
    success = create_batch_modification_table(app)
    
    if success:
        logger.info("\n" + "=" * 60)
        logger.info("Migration completed successfully! ✓")
        logger.info("=" * 60)
        logger.info("\nYou can now use the batch resume modification feature:")
        logger.info("  POST /api/resume/batch-modify")
        logger.info("  GET  /api/resume/batch-modify/<batch_id>")
        logger.info("  GET  /api/resume/batch-modify/history")
    else:
        logger.error("\n" + "=" * 60)
        logger.error("Migration failed! ✗")
        logger.error("=" * 60)
