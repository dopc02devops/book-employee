FROM nginx:1.21-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY custom_404.html /var/www/html/
COPY custom_500.html /var/www/html/
COPY custom_502.html /var/www/html/
COPY custom_503.html /var/www/html/
COPY index.html /var/www/html/
COPY nginx.conf /etc/nginx/conf.d

LABEL "com.datadoghq.ad.check_names"='["nginx"]'
LABEL "com.datadoghq.ad.init_configs"='[{}]'
LABEL "com.datadoghq.ad.instances"='[{"nginx_status_url": "http://%%host%%:%%port%%/nginx_status"}]'
LABEL "com.datadoghq.ad.logs"='[{"source": "nginx", "service": "nginx-service"}]'