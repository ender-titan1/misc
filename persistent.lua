local DIR = "persistent_data/" 
local allPersistent = {}

--function init_target(path)
--    if not fs.exists(DIR) then
--        fs.makeDir(DIR)
--    end
--end

PersistentData = {data = 0, name = ""}

function PersistentData:new(data, name)
    o = {}
    setmetatable(o, self)
    self.__index = self
    self.data = data
    self.name = name
    allPersistent[name] = data
    return o
end

function PersistentData:__call()
    return self.data
end

function PersistentData:set(data)
    self.data = data
    allPersistent[self.name] = self.data
    return data
end

pData = PersistentData:new(0, "data1")
pData:set(2)

print(pData())

