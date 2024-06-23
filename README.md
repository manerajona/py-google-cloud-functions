# Python Google Cloud-Functions

## Install Dependencies
To install these dependencies, you would:

1. Navigate to the directory containing `requirements.txt`.

2. Run the installation command:
    ```shell
    pip install -r requirements.txt
    ```

## Virtual Environment (Recommended)
It is generally a good practice to use a virtual environment to manage your project's dependencies. 
This ensures that the dependencies required by different projects are isolated from each other.

Steps to use a virtual environment:

1. Create a virtual environment:
    ```shell
    python -m venv myenv
    ```

2. Activate the virtual environment:
    - On Widows:
    ```shell
    myenv\Scripts\activate
    ```
   - On Linux/Mac:
   ```shell
    source myenv/bin/activate
    ```

3. Install dependencies:
    ```shell
    pip install -r requirements.txt
    ```

4. Deactivate the virtual environment when done:
    - On Widows:
    ```shell
    myenv\Scripts\deactivate
    ```
    - On Linux/Mac:
   ```shell
    source myenv/bin/deactivate
    ```

Using a virtual environment helps avoid conflicts between different projects' dependencies and keeps your global Python environment clean.