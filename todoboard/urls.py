from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'todo.views.index', name='collaborate.views.index'),
    url(r'^rickandmorty/$', 'todo.views.rickandmorty', name='collaborate.views.rickandmorty'),
    url(r'^new_user/$', 'todo.views.new_user'),
    url(r'^new_board/$', 'todo.views.new_board'),
    url(r'^(?P<board_id>\d+)/new_task/$', 'todo.views.new_task'),
    url(r'^complete/(?P<task_id>\d+)/$', 'todo.views.complete_task'),
    url(r'^delete/(?P<board_id>\d+)/$', 'todo.views.delete_board'),
    url(r'^login/$', 'todo.views.login_user', name='login'),
    url(r'^logout/$', 'todo.views.logout_user', name='logout'),
    url(r'^about/$', 'todo.views.about'),
    )
