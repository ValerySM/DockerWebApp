FROM nginx:latest

# Copy our Nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Optionally: Copy additional configuration files, if any
# COPY conf.d/ /etc/nginx/conf.d/

# Optionally: If you have your own static files to be served by Nginx
# COPY html/ /usr/share/nginx/html/

# Open port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]