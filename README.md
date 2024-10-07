# Asset Manager

This **asset manager** can be used to store **assets** and **textures**, create **materials** and **assign** them to assets. It has a **standalone** version that is used to store files and create materials, and a **maya plugin** to import assets and textures directly to the current scene.

## Standalone App

### Interface

In the standalone app, you will find in the **top left**, the buttons to import assets and textures and a button to create materials.
In the **center**, you have a list of all assets stored (mesh, textures and materials).
In the **top right**, you can filter the list of assets (mesh, textures and materials, or everything), and a search bar to filter by name.

![Standalone Application](./assets/readme/standalone.jpg)

### Import assets

Once clicked on the **Import Asset** button. It will show a window where you can give a **name**, **path** and **material** to the asset.

![Import Asset](./assets/readme/import_asset.jpg)

### Import textures

Once clicked on the **Import Texture** button. It will show a window where you can give a **name** and to the texture.

![Import Texture](./assets/readme/import_texture.jpg)


### Note that for assets or textures, you can also drag and drop files directly into the app to import them


### Create Material

Once clicked on the **Create Material** button. It will show a window where you can give a **name** and select all the **textures** you want to add the material.

![Create Material](./assets/readme/create_material.jpg)


### Note that you can edit at any time any items by clicking on it

## Maya Plugin

Once in Maya, you can open the **Asset Manager Window**. In this window, you can click on any item you want to import.

![Maya Plugin](./assets/readme/maya.jpg)

For meshes you can choose to import **as reference**.

![Maya Mesh](./assets/readme/maya_mesh.jpg)

For materials you can choose to import and **assign materials to selected meshes**.

![Maya Material](./assets/readme/maya_material.jpg)