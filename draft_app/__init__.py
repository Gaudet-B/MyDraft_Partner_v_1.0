from flask import Flask, render_template, redirect, request, session, flash
app = Flask(__name__)
app.secret_key = "sssecrrettt"