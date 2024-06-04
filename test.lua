LEVEL = 1
PROTOCOL = "elevator:1"
os.loadAPI("button")
os.loadAPI("persistent")

local currentLevel = PersistentData:new(0, "level")

function init()
    rednet.open("top")
end

function call()
    redstone.setAnalogOutput("back", LEVEL)

    wait_for_signal(LEVEL)
end

function go_to_level(level)
    redstone.setAnalogOutput("back", level)

    -- if the target level is higher than the computer's level
    -- then make sure the gearshift is powered correctly
    redstone.setOutput("left", level > currentLevel())

    wait_for_signal(level)
end

function wait_for_signal(level)
    -- wait for the elevator to signal that it has switched to the
    -- correct floor (there's only one input into the computer)
    os.pullEvent("redstone")

    -- sync the current elevator level 
    rednet.broadcast(level, PROTOCOL)
    currentLevel.

end
