--assert(loadfile("send_data.lua"))("stuff")
sk = net.createConnection(net.TCP, 0)
out_str = ...
sk:on("receive", function(sck, c) print(c) end )
sk:on("connection", function(sck,c)
    -- Wait for connection before sending.
    sk:send(out_str)
end)
sk:connect(5001,"192.227.175.138")
