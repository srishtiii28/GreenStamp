const { ethers } = require("hardhat");

async function main() {
  const [deployer] = await ethers.getSigners();
  console.log("Deploying contracts with the account:", deployer.address);

  const GreenStamp = await ethers.getContractFactory("GreenStamp");
  const greenStamp = await GreenStamp.deploy();
  
  await greenStamp.deployed();
  
  console.log("GreenStamp deployed to:", greenStamp.address);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  }); 