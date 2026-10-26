# Slim Debian with Python 3.14, the version requirements.txt was frozen with.
FROM python:3.14-slim

# No .pyc files in the image, and logs printed at once instead of buffered.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Every following instruction runs inside this folder of the image.
WORKDIR /app

# Dependencies before the code: Docker reuses this step as long as requirements.txt is unchanged.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Then the project code, minus everything listed in .dockerignore.
COPY . .

# Gather the static files (site and admin) into staticfiles/ for WhiteNoise.
# settings.py requires a SECRET_KEY to load: a throwaway one, given to this command only, is enough.
RUN SECRET_KEY=build-only python manage.py collectstatic --noinput

# Run the site as an unprivileged user, not root. It owns /app so SQLite can write sessions.
RUN useradd appuser && chown -R appuser /app
USER appuser

# The port gunicorn listens on (documentation only: docker run -p opens it).
EXPOSE 8000

# Started at each container launch: gunicorn on the WSGI entry point, reachable from outside.
# The control socket is disabled: nobody pilots gunicorn from inside the container.
CMD ["gunicorn", "oc_lettings_site.wsgi", "--bind", "0.0.0.0:8000", "--workers", "2", "--no-control-socket"]
