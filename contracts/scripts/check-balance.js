const { ethers } = require("hardhat");

async function main() {
  const address = "0x79BDD9e69b4C24d951d0ED1748E2582373a4235e";
  const balance = await ethers.provider.getBalance(address);
  console.log("Balance:", ethers.utils.formatEther(balance), "EDU");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  }); 