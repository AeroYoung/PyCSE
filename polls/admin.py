from django.contrib import admin

from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3  # 默认提供 3 个足够的选项字段


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    search_fields = ['question_text']
    list_filter = ['pub_date']
    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)
