from channels.consumer import AsyncConsumer
from .models import *
import asyncio
from channels.db import database_sync_to_async
from django.shortcuts import render, redirect
from .forms import PostForm, PostForm2
from .models import Post
from django.core.exceptions import ObjectDoesNotExist


