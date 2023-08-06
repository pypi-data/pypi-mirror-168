# Robot Manager

Robot Manager is a package that allows to connect with iBott **robot manager console** to use cloud features.
visit https://ibott.io/Academy/robot-manager to learn more about the robot manager features.


## Bot Class

create_queue(queue_name): Create a queue.
find_queue_by_id(queue_id): Find a queue by its ID.
find_queues_by_name(queue_name): Find all queues by its name.
get_asset_by_name(asset_name): Get an asset by its name.
get_asset_by_id(asset_id): Get an asset by its ID.
save_file_from_console(file_path, file_name): Save a file from the Orchestrator API.

## Queue Class

create_item(item_data): Create a new item in the queue.
get_next_item(): Get the next pending item in the queue.
set_retry_times(times): Set the retry times of an item.

## Item Class

set_item_as_working(self): Set item as working.
set_item_as_ok(self): Set item as ok.
set_item_as_fail(self): Set item as failed.
set_item_as_pending(self): Set item as pending.
set_item_executions(self): increment item execution counter
## Asset Class

get_assets(): Get assets all assets from the robot manager console.
get_asset_by_id(): Get asset by ID from the robot manager console. 
get_asset_by_name(): Get asset by name from the robot manager console.