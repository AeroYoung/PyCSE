from django.contrib import admin
from .models import Category, Topic, Practice, PracticeStatistic


class TopicInline(admin.TabularInline):
    model = Topic
    extra = 3  # 默认提供 3 个足够的选项字段


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'category_num')
    fieldsets = [
        (None, {'fields': ['category_name']})
    ]
    inlines = [TopicInline]


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('category', 'topic_name', 'topic_num', 'single_score', 'total_score', 'probability_str')
    fieldsets = [
        (None, {'fields': ['category', 'topic_name', 'topic_num', 'single_score']}),
    ]
    search_fields = ['topic_name']
    list_filter = ['category__category_name']


@admin.register(Practice)
class PracticeAdmin(admin.ModelAdmin):
    list_display = ('topic_str', 'practice_num', 'time_info',
                    'score_without_time', 'probability_without_time_str', 'score', 'probability_str',
                    'error_num', 'error_probability_str', 'weight',
                    'user', 'practice_date')
    search_fields = ['topic__topic_name']
    list_filter = ['topic__category__category_name', 'topic__topic_name']


admin.register(PracticeStatistic)