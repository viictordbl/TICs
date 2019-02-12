channelID1 = 694049;
readApiKey1='LLEPG07A5VHE2UOT';
channelID2 = 694050;
readApiKey2='4SNAOLWA8LAS7LS0';
N = 64;
[data1,time1]=thingSpeakRead(channelID1,'ReadKey',readApiKey1,'Fields',[1,2],'NumPoints',N);
[data2,time2]=thingSpeakRead(channelID2,'ReadKey',readApiKey2,'Fields',[1,2],'NumPoints',N);

%Temperatura
k=1;
j=1;
for i=1:(length(data1)+length(data2))
    if (mod(i,2) ==0)
        data(i,1) = data2(j,1);
        time(i) = time2(j);
        j=j+1;
    else
        data(i,1) = data1(k,1);
        time(i) = time1(k);
        k = k+1;
    end
end

%Humedad
k=1;
j=1;
for i=1:(length(data1)+length(data2))
    if (mod(i,2) ==0)
        data(i,2) = data2(j,2);
        time(i) = time2(j);
        j=j+1;
    else
        data(i,2) = data1(k,2);
        time(i) = time1(k);
        k = k+1;
    end
end

figure(1);
plot(time,data(:,1));
title('Temperature');
xlabel('Time');
ylabel('T (ºC)');

hold on;

figure(2);
plot(time,data(:,2));
title('Humidity');
xlabel('Time');
ylabel('%');

%% REGULADOR TEMPERATURA INVERNADERO %%

% almacenamos los valores de temperatura adquiridos 
temp = data(:,1);
% definimos la funcion de transferencia de nuestro invernadero
s=tf('s');
sys=1/(50*s+1);
% discretizar el sistema con el tiempo de muestreo de la toma de datos
sys_d=c2d(sys,10);
% estudiamos la dinamica del sistema
t=0:10:1279;
t=t';
y=lsim(sys_d,temp,t);
figure(3);
plot(t,y);
% diseñamos el controlador para que se adapte a nuestras exigencias
C=(2*(50*s+1))/(50*s);
% comparamos las mejoras en las características de la respuesta
sys_lc=feedback(C*sys,1);
sys_lc_d=c2d(sys_lc,10);
y_lc=lsim(sys_lc_d,temp,t);
hold on;
plot(t,y_lc);
xlabel('segundos')
ylabel('temperatura ºC')
legend('original','PI')