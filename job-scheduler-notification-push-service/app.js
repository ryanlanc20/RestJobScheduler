const {Server} = require("socket.io");
const http = require("http");
const amqp = require("amqplib/callback_api")

const server = http.createServer();

const io = new Server(server,{
    cors: {
      origin: "*",
      methods: ["GET", "POST"]
    }
});

io.on("connection",(socket) => {
    console.log("Connection...");
    io.emit("notification",{"type":"job_complete"});
});

amqp.connect("amqp://notifications_queue?heartbeat=5",function(error0,connection){
    if (error0){
        throw error0;
    }
    connection.createChannel(function(error1,channel){
        if (error1){
            throw error1;
        }

        // Periodic connection check (app terminates if queue push fails, allowing docker to restart, etc...)
        setInterval(function(){
            channel.assertQueue("connection-test",{"durable":false});
            channel.sendToQueue("connection-test",Buffer.from("Testing connection"));
            channel.consume("connection-test",function(msg){
                console.log("Consumed connection test");
            });
        },2000);

        channel.assertQueue("notifications",{"durable":false});

        channel.consume("notifications", function(msg){
            io.emit("notification",msg.content.toString());
            console.log("Consumed notification");
        });
    });
});

io.listen(9030,() => "Notifications server started");