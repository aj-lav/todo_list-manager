from flask import Flask,render_template,request,url_for,Blueprint

bp = Blueprint('auth', 'auth', url_prefix='/auth')
