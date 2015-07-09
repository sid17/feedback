from django.db import models
from djangotoolbox.fields import ListField,DictField
from datetime import datetime
from django.db.models.signals import post_save

class e2eFeedback(models.Model):
	actualInput=models.TextField()
	tellmedaveOutput= ListField(ListField())
	videoPath=models.TextField()
	tellmedaveFeedback = ListField(ListField())
	planitFeedback = ListField(DictField())

	tellmedaveFeedbackText = ListField()
	planitFeedbackText = ListField()

	created_at = models.DateTimeField(default=datetime.now())
	feedId = models.TextField(db_index=True)
	meta = {'indexes':['feedId']}
	upvotes = models.IntegerField(default=0)
	downvotes = models.IntegerField(default=0)
	

	def to_json(self):
		return {"_id":self.id,
			"actualInput" : self.actualInput,
			"tellmedaveOutput" : self.tellmedaveOutput[-1],
			"videoPath" : self.videoPath,
			"feedId":self.feedId,
			"upvotes":self.upvotes,
			"downvotes":self.downvotes,
			}

	class Meta:
		db_table = 'e2eFeedback'
		get_latest_by = 'created_at'

class nlpFeedback(models.Model):
	envNumber=models.TextField()
	NLPInstruction= models.TextField()
	created_at = models.DateTimeField(default=datetime.now())
	
	def to_json(self):
		return {"_id":self.id,
			"envNumber" : self.envNumber,
			"NLPInstruction" : self.NLPInstruction,
			}

	class Meta:
		db_table = 'nlpFeedback'
		get_latest_by = 'created_at'

