from pyke.krb_compiler import compile_krb
import os

# 1. Define the PyKE knowledge package name (folder name) for compiled rules
generated_pkg_name = "wallet"

# 2. Define base directory and output directory for compiled files
base_dir = os.path.dirname(__file__)
compiled_dir = os.path.join(base_dir, generated_pkg_name)

# 3. Path to the source .krb file
krb_file = os.path.join(base_dir, "wallet_rules.krb")

# 4. Ensure the output directory exists and is a Python package
os.makedirs(compiled_dir, exist_ok=True)
init_file = os.path.join(compiled_dir, "__init__.py")
if not os.path.exists(init_file):
    open(init_file, "w").close()

# 5. Compile the .krb file into the target package
# Signature: compile_krb(source_package, target_package, target_dir, krb_filepath)
compile_krb(
    generated_pkg_name,    # source package name ("wallet")
    generated_pkg_name,    # target package name ("wallet")
    compiled_dir,          # directory for compiled output
    krb_file               # path to the source .krb file
)

print("✅ Compilation successful!")
