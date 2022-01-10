# FaceClustering

```mermaid
classDiagram
  direction RL
  class Images {
    -hash[PK]: str
    -file_path: str
  }
  class Locations{
    -id[PK]: int
    -image_hash: str
    -label_id: str
    -box: list[int]
    -encoding: blob
  }
  class Labels{
    -id[PK]: int
    -name: str
  }
  Locations "*" --o "1" Images : image_hash
  Locations "1" --o "1" Labels : label_id
  ```