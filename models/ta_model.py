from database.db_connection import Database
from mysql.connector import Error

class TAModel:
    def __init__(self):
        self.db = Database()
        
    
    def get_ta_by_id_password(self, userID, password):
        query = "SELECT * FROM User WHERE userID = %s AND password = %s AND role = 'TA'"
        try:
            cursor = self.db.execute_query(query, (userID, password))
            if cursor is None:
                raise Exception("Query Execution Failed!!!!")
            return cursor.fetchone()
        except Exception as e:
            print(f"Failed to get TA '{userID}': {e}")
            return None
    def update_password(self, userID, password):
        query = "UPDATE User SET password = %s WHERE userID = %s"
        try:
            self.db.execute_query(query, (password, userID))
            self.db.connection.commit()
        except Exception as e:
            print(f"Failed to update password for TA '{userID}': {e}")

    def get_courses_by_userID(self, TAID):
        query = """
                SELECT ac.uToken, c.courseID, c.title, c.textBookID
                FROM ActiveCourseTA acta
                JOIN ActiveCourse ac ON acta.uToken = ac.uToken
                JOIN Course c ON ac.courseID = c.courseID
                WHERE acta.TAID = %s
                """
        try:
            cursor = self.db.execute_query(query, (TAID,))
            if cursor is None:
                raise Exception("Query Execution Failed!!!!")
            return cursor.fetchall()
        except Exception as e:
            print(f"Failed to get courses for TA '{TAID}': {e}")
            return None
        
    def get_students_by_courseID(self, courseID):
        query = """
                SELECT ae.studentID
                FROM ActiveEnrollment ae
                JOIN ActiveCourse ac ON ae.uToken = ac.uToken
                WHERE ac.courseID = %s AND ae.c_status = 'Enrolled'
                """
        try:
            cursor = self.db.execute_query(query, (courseID,))
            if cursor is None:
                raise Exception("Query Execution Failed!!!!")
            return cursor.fetchall()
        except Exception as e:
            print(f"Failed to get students for course '{courseID}': {e}")
            return None

    def getchapterByTextBookId_chapterID(self, ebook):
        textBookID, chapterID, userID = ebook['textBookID'], ebook['chapterID'], ebook['userID']
        query = "SELECT * FROM Chapter WHERE textBookID = %s AND chapterID = %s"
        try:
            cursor = self.db.execute_query(query, (textBookID, chapterID,))
            if cursor is None:
                raise Exception("Query Execution Failed!!!!")
            return cursor.fetchone()
        except Exception as e:
            print(f"Failed to get chapterID with textBookID {chapterID}, {textBookID}: {e}")
            return None
    def addChapter(self, ebook):
        chapterID, chapterTitle, textBookID, userID = ebook['chapterID'], ebook['chapterTitle'], ebook['textBookID'], ebook['userID']
        query = "INSERT INTO Chapter (chapterID, title, textBookID, userID) VALUES (%s, %s, %s, %s)"
        try:
            cursor = self.db.execute_query(query, (chapterID, chapterTitle, textBookID, userID))
            if cursor is None:
                raise Exception("Query Execution Failed!!!!")
            print(f"Chapter '{chapterTitle}' created successfully!")
            return 1
        except Exception as e:
            print(f"Failed to create Chapter '{chapterTitle}': {e}")
            return 0  
    def getSectionByChapterID_SectionID(self, ebook):
        textBookID, chapterID, sectionID, userID = ebook['textBookID'], ebook['chapterID'], ebook['sectionID'], ebook['userID']
        query = "SELECT * FROM Section WHERE textBookID=%s AND chapterID = %s AND sectionID = %s"
        try:
            cursor = self.db.execute_query(query, (textBookID, chapterID, sectionID,))
            if cursor is None:
                raise Exception("Query Execution Failed!!!!")
            return cursor.fetchone()
        except Exception as e:
            print(f"Failed to get Section with chapterID {chapterID}, sectionID {sectionID}: {e}")
            return None
    def addSection(self, ebook):
        sectionID, title, textBookID, chapterID, userID = ebook['sectionID'], ebook['sectionTitle'], ebook['textBookID'], ebook['chapterID'], ebook['userID']
        query = "INSERT INTO Section (sectionID, title, textBookID, chapterID, userID) VALUES (%s, %s, %s, %s, %s)"
        try:
            cursor = self.db.execute_query(query, (sectionID, title, textBookID, chapterID, userID))
            if cursor is None:
                raise Exception("Query Execution Failed!!!!")
            print(f"Section '{title}' created successfully!")
            return 1
        except Exception as e:
            print(f"Failed to create Section '{title}': {e}")
            return 0
        
    def getContentBlock(self, ebook):
        blockID, blockType, textBookID, chapterID, sectionID, userID = ebook['contentblockID'], ebook['blockType'], ebook['textBookID'], ebook['chapterID'], ebook['sectionID'], ebook['userID']
        query = "SELECT * FROM ContentBlock WHERE blockID = %s AND blockType = %s AND textBookID = %s AND chapterID = %s AND sectionID = %s"
        try:
            cursor = self.db.execute_query(query, (blockID, blockType, textBookID, chapterID, sectionID,))
            if cursor is None:
                raise Exception("Query Execution Failed!!!!")
            return cursor.fetchone()
        except Exception as e:
            print(f"Failed to get Text block with ID {blockID}: {e}")
            return None
        
    def addContentBlock(self, ebook):
        blockID, blockType, content, textBookID, chapterID, sectionID, userID = ebook['contentblockID'], ebook['blockType'], ebook['content'], ebook['textBookID'], ebook['chapterID'], ebook['sectionID'], ebook['userID']
        query = "INSERT INTO ContentBlock (blockID, blockType, content, textBookID, chapterID, sectionID, userID) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        try:
            cursor = self.db.execute_query(query, (blockID, blockType, content, textBookID, chapterID, sectionID, userID))
            if cursor is None:
                raise Exception("Query Execution Failed!!!!")
            print(f"Text block '{blockID}' with '{type}' created successfully!")
            return 1
        except Exception as e:
            print(f"Failed to create Text block '{blockID}' with '{type}': {e}")
            return 0    
        
    def addContentTransaction(self, ebook):
        try:
            if not self.db.connection.in_transaction:
                self.db.connection.start_transaction()
            if(self.getchapterByTextBookId_chapterID(ebook) is None):
                self.addChapter(ebook)
            if(self.getSectionByChapterID_SectionID(ebook) is None):
                self.addSection(ebook)
            if(self.getContentBlock(ebook) is None):
                self.addContentBlock(ebook)
            else:
                print("You can not add the content block as it already exists. You can modify it.")
            self.db.connection.commit()
            return 1
        except Error as e:
            if self.db.connection.is_connected():
                self.db.connection.rollback()
                print("Transaction rolled back due to error:", e)
            return 0
        
    def getQuestionById(self, ebook):
        questionID, activityID, blockID, sectionID, chapterID, textBookID, userID = ebook['questionID'], ebook['activityID'], ebook['contentblockID'], ebook['sectionID'], ebook['chapterID'], ebook['textBookID'], ebook['userID']
        query = "SELECT * FROM Question WHERE questionID = %s AND activityID = %s AND blockID = %s AND sectionID = %s AND chapterID = %s AND textBookID = %s"
        try:
            cursor = self.db.execute_query(query, (questionID, activityID, blockID, sectionID, chapterID, textBookID,))
            if cursor is None:
                raise Exception("Query Execution Failed!!!!")
            return cursor.fetchone()
        except Exception as e:
            print(f"Failed to get Question with ID {questionID}: {e}")
            return None
        
    def addQuestion(self, ebook):
        questionID, textBookID, chapterID, sectionID, blockID, activityID, question, OP1, OP1_EXP, OP1_Label, OP2, OP2_EXP, OP2_Label, OP3, OP3_EXP, OP3_Label, OP4, OP4_EXP, OP4_Label, userID = ebook['questionID'], ebook['textBookID'], ebook['chapterID'], ebook['sectionID'], ebook['contentblockID'], ebook['activityID'], ebook['question'], ebook['OP1'], ebook['OP1_EXP'], ebook['OP1_Label'], ebook['OP2'], ebook['OP2_EXP'], ebook['OP2_Label'], ebook['OP3'], ebook['OP3_EXP'], ebook['OP3_Label'], ebook['OP4'], ebook['OP4_EXP'], ebook['OP4_Label'], ebook['userID']
        query = "INSERT INTO Question (questionID, textBookID, chapterID, sectionID, blockID, activityID, question, OP1, OP1_EXP, OP1_Label, OP2, OP2_EXP, OP2_Label, OP3, OP3_EXP, OP3_Label, OP4, OP4_EXP, OP4_Label, userID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        try:
            cursor = self.db.execute_query(query, (questionID, textBookID, chapterID, sectionID, blockID, activityID, question, OP1, OP1_EXP, OP1_Label, OP2, OP2_EXP, OP2_Label, OP3, OP3_EXP, OP3_Label, OP4, OP4_EXP, OP4_Label, userID))
            if cursor is None:
                raise Exception("Query Execution Failed!!!!")
            print(f"Question '{questionID}' created successfully!")
            return 1
        except Exception as e:
            print(f"Failed to create Question '{questionID}': {e}")
            return 0
    
    def getActivtyById(self, ebook):
        activityID, textBookID, chapterID, sectionID, blockID, userID = ebook['activityID'], ebook['textBookID'], ebook['chapterID'], ebook['sectionID'], ebook['contentblockID'], ebook['userID']
        query = "SELECT * FROM Activity WHERE activityID = %s AND textBookID = %s AND chapterID = %s AND sectionID = %s AND blockID = %s"
        try:
            cursor = self.db.execute_query(query, (activityID, textBookID, chapterID, sectionID, blockID,))
            if cursor is None:
                raise Exception("Query Execution Failed!!!!")
            return cursor.fetchone()
        except Exception as e:
            print(f"Failed to get Activity with ID {activityID}: {e}")
            return None
        
    def addActivity(self, ebook):
        activityID, textBookID, chapterID, sectionID, blockID, userID = ebook['activityID'], ebook['textBookID'], ebook['chapterID'], ebook['sectionID'], ebook['contentblockID'], ebook['userID']
        query = "INSERT INTO Activity (activityID, textBookID, chapterID, sectionID, blockID, userID) VALUES (%s, %s, %s, %s, %s, %s)"
        try:
            cursor = self.db.execute_query(query, (activityID, textBookID, chapterID, sectionID, blockID, userID))
            if cursor is None:
                raise Exception("Query Execution Failed!!!!")
            print(f"Activity '{activityID}' created successfully!")
            return 1
        except Exception as e:
            print(f"Failed to create Activity '{activityID}': {e}")
            return 0
    def addActivtyTransaction(self, ebook):
        try:
            if not self.db.connection.in_transaction:
                self.db.connection.start_transaction()
            if(self.getchapterByTextBookId_chapterID(ebook) is None):
                self.addChapter(ebook)
            if(self.getSectionByChapterID_SectionID(ebook) is None):
                self.addSection(ebook)
            if(self.getContentBlock(ebook) is None):
                self.addContentBlock(ebook)
            if(self.getActivtyById(ebook) is None):
                self.addActivity(ebook)
            if(self.getQuestionById(ebook) is None):
                self.addQuestion(ebook)
            else:
                print("You can not add the same question ID as it already exists. You can modify it.")
            
            self.db.connection.commit()
            return 1
        except Error as e:
            if self.db.connection.is_connected():
                self.db.connection.rollback()
                print("Transaction rolled back due to error:", e)
            return 0
        
    def is_allowed_to_modify_for_text_picture(self, ebook):
        blockID, blockType, textBookID, chapterID, sectionID, userID = ebook['contentblockID'], ebook['blockType'], ebook['textBookID'], ebook['chapterID'], ebook['sectionID'], ebook['userID']
        query = "SELECT role from User where userID = (SELECT userID FROM ContentBlock WHERE blockID = %s AND blockType = %s AND textBookID = %s AND chapterID = %s AND sectionID = %s)"
        try:
            cursor = self.db.execute_query(query, (blockID, blockType, textBookID, chapterID, sectionID,))
            if cursor is None:
                raise Exception("Query Execution Failed!!!!")
            result = cursor.fetchone()
            if result is None:
                return False
            role = result[0]
            return role != 'Admin'
        except Exception as e:
            print(f"Failed to get Text block with ID {blockID}: {e}")
            return None
    def is_allowed_to_modify_for_activity_question(self, ebook):
        questionID, activityID, blockID, sectionID, chapterID, textBookID, userID = ebook['questionID'], ebook['activityID'], ebook['contentblockID'], ebook['sectionID'], ebook['chapterID'], ebook['textBookID'], ebook['userID']
        query = "SELECT role from User where userID = (SELECT userID FROM Question WHERE questionID = %s AND activityID = %s AND blockID = %s AND sectionID = %s AND chapterID = %s AND textBookID = %s)"
        try:
            cursor = self.db.execute_query(query, (questionID, activityID, blockID, sectionID, chapterID, textBookID,))
            if cursor is None:
                raise Exception("Query Execution Failed!!!!")
            result = cursor.fetchone()
            if result is None:
                return False
            role = result[0]
            return role != 'Admin'
        except Exception as e:
            print(f"Failed to get Question with ID {questionID}: {e}")
            return None
        
    def is_ta_in_course(self, TAID, courseID):
        query = """
            SELECT COUNT(*)
            FROM ETextBook.ActiveCourseTA acta
            JOIN ETextBook.ActiveCourse ac ON acta.uToken = ac.uToken
            WHERE acta.TAID = %s AND ac.courseID = %s
        """
        try:
            cursor = self.db.execute_query(query, (TAID, courseID))
            if cursor is None:
                raise Exception("Query Execution Failed!!!!")
            result = cursor.fetchone()
            return result[0] > 0
        except Exception as e:
            print(f"Failed to check if TA '{TAID}' is in course '{courseID}': {e}")
            return False
    
    def update_modifiedContentBlock(self, ebook):
        blockID, blockType, content, textBookID, chapterID, sectionID, userID = ebook['contentblockID'], ebook['blockType'], ebook['content'], ebook['textBookID'], ebook['chapterID'], ebook['sectionID'], ebook['userID']
        query = "UPDATE ContentBlock SET content = %s, userID = %s WHERE blockID = %s AND blockType = %s AND textBookID = %s AND chapterID = %s AND sectionID = %s"
        try:
            cursor = self.db.execute_query(query, (content, userID, blockID, blockType, textBookID, chapterID, sectionID,))
            if cursor is None:
                raise Exception("Query Execution Failed!!!!")
            print(f"Content block '{blockID}' with '{type}' updated successfully!")
            return 1
        except Exception as e:
            print(f"Failed to update Content block '{blockID}' with '{type}': {e}")
            return 0
        
    def update_modifiedActivityQuestion(self, ebook):
        questionID, textBookID, chapterID, sectionID, blockID, activityID, question, OP1, OP1_EXP, OP1_Label, OP2, OP2_EXP, OP2_Label, OP3, OP3_EXP, OP3_Label, OP4, OP4_EXP, OP4_Label, userID = ebook['questionID'], ebook['textBookID'], ebook['chapterID'], ebook['sectionID'], ebook['contentblockID'], ebook['activityID'], ebook['question'], ebook['OP1'], ebook['OP1_EXP'], ebook['OP1_Label'], ebook['OP2'], ebook['OP2_EXP'], ebook['OP2_Label'], ebook['OP3'], ebook['OP3_EXP'], ebook['OP3_Label'], ebook['OP4'], ebook['OP4_EXP'], ebook['OP4_Label'], ebook['userID']
        query = "UPDATE Question SET question = %s, userID = %s, OP1 = %s, OP1_EXP = %s, OP1_Label = %s, OP2 = %s, OP2_EXP = %s, OP2_Label = %s, OP3 = %s, OP3_EXP = %s, OP3_Label = %s, OP4 = %s, OP4_EXP = %s, OP4_Label = %s WHERE questionID = %s AND activityID = %s AND blockID = %s AND sectionID = %s AND chapterID = %s AND textBookID = %s"
        try:
            cursor = self.db.execute_query(query, (question, userID, OP1, OP1_EXP, OP1_Label, OP2, OP2_EXP, OP2_Label, OP3, OP3_EXP, OP3_Label, OP4, OP4_EXP, OP4_Label, questionID, activityID, blockID, sectionID, chapterID, textBookID,))
            if cursor is None:
                raise Exception("Query Execution Failed!!!!")
            print(f"Question '{questionID}' updated successfully!")
            return 1
        except Exception as e:
            print(f"Failed to update Question '{questionID}': {e}")
            return 0
    
    
    def modifyContentTransaction(self, ebook, type):
        try:
            if not self.db.connection.in_transaction:
                self.db.connection.start_transaction()
            if(self.getContentBlock(ebook) is not None):
                if type == "text" or type == "picture":
                    if self.is_allowed_to_modify_for_text_picture(ebook):
                        self.update_modifiedContentBlock(ebook)
                    else:
                        print("You can not modify the content block as you are not allowed to modify it.")
                elif type == "activity":
                    if self.is_allowed_to_modify_for_activity_question(ebook):
                        self.update_modifiedActivityQuestion(ebook)
                    else:
                        print("You can not modify the content block as you are not allowed to modify it.")
            else:
                print("You can not modify the content block as it does not exist. You can add it.")
            self.db.connection.commit()
            return 1
        except Error as e:
            if self.db.connection.is_connected():
                self.db.connection.rollback()
                print("Transaction rolled back due to error:", e)
            return 0
        
    def deleteContentBlock(self, ebook):
        blockID = ebook['contentblockID']
        textBookID = ebook['textBookID']
        chapterID = ebook['chapterID']
        sectionID = ebook['sectionID']
        userID = ebook['userID']
        
        query = """
            DELETE cb
            FROM ContentBlock cb
            JOIN User u ON u.userID = cb.userID
            WHERE cb.blockID = %s AND cb.textBookID = %s AND cb.chapterID = %s AND cb.sectionID = %s 
            AND u.role = 'TA'
        """
        
        try:
            cursor = self.db.execute_query(query, (blockID, textBookID, chapterID, sectionID))
            if cursor is None:
                raise Exception("Query Execution Failed!!!!")
            if cursor.rowcount == 0:
                print(f"No content block with ID '{blockID}' was deleted. You do not have permission to delete it.")
                return 0
            print(f"Content block '{blockID}' deleted successfully!")
            print(f"Text block '{blockID}' deleted successfully!")
            self.db.connection.commit()
            return 1
        except Exception as e:
            print(f"Failed to delete Text block '{blockID}': {e}")
            return 0
        
    def iscontentBlockExists_in_content_user_activity(self, ebook):
        blockID = ebook['contentblockID']
        textBookID = ebook['textBookID']
        chapterID = ebook['chapterID']
        sectionID = ebook['sectionID']
        userID = ebook['userID']
        courseID = ebook['courseID']
        
        query = """
            SELECT COUNT(*)
            FROM ETextBook.content_user_activity
            WHERE blockID = %s AND textBookID = %s AND chapterID = %s AND sectionID = %s AND courseID = %s
        """
        
        try:
            cursor = self.db.execute_query(query, (blockID, textBookID, chapterID, sectionID, courseID))
            if cursor is None:
                raise Exception("Query Execution Failed!!!!")
            result = cursor.fetchone()
            return result[0] > 0
        except Exception as e:
            print(f"Failed to check if content block '{blockID}' exists in content_user_activity: {e}")
            return False
        
    def checkHiddenStatusforblock(self, ebook):
        blockID = ebook['contentblockID']
        textBookID = ebook['textBookID']
        chapterID = ebook['chapterID']
        sectionID = ebook['sectionID']
        userID = ebook['userID']
        courseID = ebook['courseID']
        
        query = """
            SELECT isHidden_block
            FROM ETextBook.content_user_activity
            WHERE blockID = %s AND textBookID = %s AND chapterID = %s AND sectionID = %s AND courseID = %s
        """
        try:
            cursor = self.db.execute_query(query, (blockID, textBookID, chapterID, sectionID, courseID))
            if cursor is None:
                raise Exception("Query Execution Failed!!!!")
            result = cursor.fetchone()
            return result[0]
        except Exception as e:
            print(f"Failed to check hidden status for block '{blockID}': {e}")
            return None  
        
        
    def hideContentBlock(self, ebook):
        blockID = ebook['contentblockID']
        textBookID = ebook['textBookID']
        chapterID = ebook['chapterID']
        sectionID = ebook['sectionID']
        userID = ebook['userID']
        courseID = ebook['courseID']
        
        if not self.iscontentBlockExists_in_content_user_activity(ebook):
            query = """
                INSERT INTO ETextBook.content_user_activity (userID, courseID, textBookID, chapterID, sectionID, blockID, isHidden_block)
                VALUES (%s, %s, %s, %s, %s, %s, 'yes')
            """
            try:
                cursor = self.db.execute_query(query, (userID, courseID, textBookID, chapterID, sectionID, blockID, ))
                if cursor is None:
                    raise Exception("Query Execution Failed!!!!")
                print(f"Content block '{blockID}' hidden successfully!")
                self.db.connection.commit()
                return 1
            except Exception as e:
                print(f"Failed to hide content block '{blockID}': {e}")
                return 0
        else:
            if self.checkHiddenStatusforblock(ebook) == 'yes':
                print(f"Content block '{blockID}' is already hidden!")
                return 1
            else:    
                query = """
                    UPDATE ETextBook.content_user_activity
                    SET isHidden_block = 'yes', userID = %s
                    WHERE blockID = %s AND textBookID = %s AND chapterID = %s AND sectionID = %s AND courseID = %s
                """
                
                try:
                    cursor = self.db.execute_query(query, (userID, blockID, textBookID, chapterID, sectionID, courseID))
                    if cursor is None:
                        raise Exception("Query Execution Failed!!!!")
                    print(f"Content block '{blockID}' hidden successfully!")
                    self.db.connection.commit()
                    return 1
                except Exception as e:
                    print(f"Failed to hide content block '{blockID}': {e}")
                    return 0