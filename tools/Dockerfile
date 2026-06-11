FROM langgenius/dify-api:1.14.2
USER root
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --break-system-packages --target=/app/api/.venv/lib/python3.12/site-packages -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
COPY app.py .
EXPOSE 80
ENTRYPOINT []
CMD ["/app/api/.venv/bin/python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
