 var socket = io();

        socket.on('connect', function() {
            console.log('Connected!');
        });

        socket.on('update_counter', function(data) {
            document.getElementById('counter').innerText = data.counter;
            if (data.counting_down) {
                document.getElementById('status').innerText = 'Counting down...';
            } else {
                document.getElementById('status').innerText = '';
            }
        });
