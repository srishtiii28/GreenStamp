const { ethers } = require("hardhat");

async function main() {
  const [deployer] = await ethers.getSigners();
  console.log("Deploying contracts with the account:", deployer.address);

  const GreenStampFactory = await ethers.getContractFactory("GreenStamp");

  // Deploy the contract normally (no manual gas limit)
  const greenStamp = await GreenStampFactory.deploy();

  await greenStamp.deployed();



  console.log("GreenStamp contract deployed to:", greenStamp.address);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("Deployment error:", error);
    process.exit(1);
  });
