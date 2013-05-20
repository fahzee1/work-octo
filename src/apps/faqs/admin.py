from django.contrib import admin

from models import Question, Tip

class QuestionAdmin(admin.ModelAdmin):
    model = Question
admin.site.register(Question, QuestionAdmin)

class TipAdmin(admin.ModelAdmin):
    model = Tip
admin.site.register(Tip, TipAdmin)