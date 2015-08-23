#=======================================================================================
# Create a Domain 
#=======================================================================================
loadProperties('properties/info.properties')

readTemplate(domainTemplate)

set("Name" , domainName)
cd('Servers/AdminServer')
set('ListenPort', int(admlistenport))

cd("/Security/" + domainName + "/User/" + adminUser)
cmo.setPassword(adminPassword)

print 'Creating Domain ' + domainHome + "/" + domainName

writeDomain(domainHome + "/" + domainName)

closeTemplate()

#=======================================================================================
# Create a DataSource 
#=======================================================================================
loadProperties('properties/info.properties')

readDomain(domainHome + domainName)

#list Diretorio
cd('/')
caminho = ls()

#DataSources and Users [DVCDTO] 
#[TODO] verificar como colocar no properties
dataSourceNames={"CaduDs":"usr_cadu", "ProdutoDs":"usr_prsv", "IcorDs":"usr_icor", "OnboardingDs":"usr_onboarding"}

for dataSourceName, dataSourceUser in dataSourceNames.items():
	print 'Creating DataSource ' + dataSourceName

	#validacao para recriar o dataSource
	if (caminho.find('JDBCSystemResource') != -1):
		delete(dataSourceName,'JDBCSystemResource')
	
	#Create Server
	cd('/')
	create(dataSourceName, 'JDBCSystemResource')
	cd('/JDBCSystemResource/' + dataSourceName)
	set('Target', adminServerName)

	#Create Url Connection
	cd('/')
	cd('/JDBCSystemResource/' + dataSourceName + '/JdbcResource/' + dataSourceName )
	create('steloJdbcDriverParams','JDBCDriverParams')
	cd('JDBCDriverParams/NO_NAME_0')
	set('DriverName', dataSourceDrive)
	set('URL', dataSourceUrl + dataSourceDvcdto)
	set('PasswordEncrypted', dataSourcePassword)
	set('UseXADataSourceInterface', 'false')
	
	#Create Properties user
	create('steloProps','Properties')
	cd('Properties/NO_NAME_0')
	create('user', 'Property')
	cd('Property/user')
	cmo.setValue(dataSourceUser)

	#Create Params Jndi
	cd('/JDBCSystemResource/' + dataSourceName + '/JdbcResource/' + dataSourceName )
	create('steloJdbcDataSourceParams','JDBCDataSourceParams')
	cd('JDBCDataSourceParams/NO_NAME_0')
	set('JNDIName',  dataSourceJndi + dataSourceName)
	set('GlobalTransactionsProtocol', dataSourceGlobalTransaction)

	#Create Test SQL Connection
	cd('/JDBCSystemResource/' + dataSourceName + '/JdbcResource/' + dataSourceName)
	create('steloJdbcConnectionPoolParams','JDBCConnectionPoolParams')
	cd('JDBCConnectionPoolParams/NO_NAME_0')
	set('TestTableName','SQL SELECT 1 FROM DUAL')


#DataSources and Users [DVTRNG]
#[TODO] verificar como colocar no properties
dataSourceNames={'GEPD':'usr_gepd', 'HSTR':'usr_hstr', 'GRSC':'usr_gers'}

for dataSourceName, dataSourceUser in dataSourceNames.items():
	print 'Creating DataSource ' + dataSourceName + dataSourceSigla

	#validacao para recriar o dataSource
	if (caminho.find('JDBCSystemResource') != -1):
		delete(dataSourceName + dataSourceSigla ,'JDBCSystemResource')
	
	#Create Server
	cd('/')
	create(dataSourceName + dataSourceSigla, 'JDBCSystemResource')
	cd('/JDBCSystemResource/' + dataSourceName + dataSourceSigla)
	set('Target', adminServerName)

	#Create Url Connection
	cd('/')
	cd('/JDBCSystemResource/' + dataSourceName + dataSourceSigla + '/JdbcResource/' + dataSourceName + dataSourceSigla)
	create('steloJdbcDriverParams','JDBCDriverParams')
	cd('JDBCDriverParams/NO_NAME_0')
	set('DriverName', dataSourceDrive)
	set('URL', dataSourceUrl + dataSourceDvtrng)
	set('PasswordEncrypted', dataSourcePassword)
	set('UseXADataSourceInterface', 'false')
	
	#Create Properties user
	create('steloProps','Properties')
	cd('Properties/NO_NAME_0')
	create('user', 'Property')
	cd('Property/user')
	cmo.setValue(dataSourceUser)

	#Create Params Jndi
	cd('/JDBCSystemResource/' + dataSourceName + dataSourceSigla + '/JdbcResource/' + dataSourceName + dataSourceSigla)
	create('steloJdbcDataSourceParams','JDBCDataSourceParams')
	cd('JDBCDataSourceParams/NO_NAME_0')
	set('JNDIName',  dataSourceJndi + dataSourceName)
	set('GlobalTransactionsProtocol', dataSourceGlobalTransaction)

	#Create Test SQL Connection
	cd('/JDBCSystemResource/' + dataSourceName + dataSourceSigla + '/JdbcResource/' + dataSourceName + dataSourceSigla)
	create('steloJdbcConnectionPoolParams','JDBCConnectionPoolParams')
	cd('JDBCConnectionPoolParams/NO_NAME_0')
	set('TestTableName','SQL SELECT 1 FROM DUAL')	

updateDomain()
closeDomain()

#=======================================================================================
# Create a JMS Queue
#=======================================================================================
loadProperties('properties/info.properties')

readDomain(domainHome + domainName)

#list Diretorio
cd('/')
caminho = ls()

if (caminho.find('JMSServer') != -1):
	delete('Stelo-JMSServer','JMSServer')

cd('/')
create('Stelo-JMSServer', 'JMSServer')


#validacao para recriar o dataSource
#if (caminho.find('JMSSystemResource') != -1):
	#delete(nameModule  + 'JmsModule', 'JMSSystemResource')

#Onboarding
cd('/')
create('OnboardingJmsModule', 'JMSSystemResource')
cd('JMSSystemResource/OnboardingJmsModule/JmsResource/NO_NAME_0')

myCF=create('OnboardingFactory','ConnectionFactory')
myCF.setJNDIName('OnboardingFactory')
myCF.setSubDeploymentName('Stelo-DISTSubDeployment')

#Cliente
distQ=create('ClienteQueue', 'UniformDistributedQueue')
distQ.setJNDIName('jms/ClienteQueue')
distQ.setSubDeploymentName('Stelo-DISTSubDeployment')

#NaoCliente
distQ=create('NaoCliente', 'UniformDistributedQueue')
distQ.setJNDIName('jms/NaoCliente')
distQ.setSubDeploymentName('Stelo-DISTSubDeployment')

cd('/')
cd('JMSSystemResource/OnboardingJmsModule')
create('Stelo-SubDeployment', 'SubDeployment')
create('Stelo-DISTSubDeployment', 'SubDeployment')

#Risco
cd('/')
create('RiscoJmsModule', 'JMSSystemResource')
cd('JMSSystemResource/RiscoJmsModule/JmsResource/NO_NAME_0')

myCF=create('ConnectionFactory','ConnectionFactory')
myCF.setJNDIName('AnaliseRiscoFactory')
myCF.setSubDeploymentName('Stelo-DISTSubDeployment')

#AnaliseRisco
distQ=create('AnaliseRiscoQueue', 'UniformDistributedQueue')
distQ.setJNDIName('jms/AnaliseRiscoQueue')
distQ.setSubDeploymentName('Stelo-DISTSubDeployment')

#RetornoAnaliseRisco
distQ=create('RetornoAnaliseRiscoQueue', 'UniformDistributedQueue')
distQ.setJNDIName('jms/RetornoAnaliseRiscoQueue')
distQ.setSubDeploymentName('Stelo-DISTSubDeployment')

cd('/')
cd('JMSSystemResource/RiscoJmsModule')
create('Stelo-SubDeployment', 'SubDeployment')
create('Stelo-DISTSubDeployment', 'SubDeployment')

#Pedido
cd('/')
create('PedidoJmsModule', 'JMSSystemResource')
cd('JMSSystemResource/PedidoJmsModule/JmsResource/NO_NAME_0')

myCF=create('PedidoFactory','ConnectionFactory')
myCF.setJNDIName('PedidoFactory')
myCF.setSubDeploymentName('Stelo-DISTSubDeployment')

#notificacao
distQ=create('NotificacaoQueue', 'UniformDistributedQueue')
distQ.setJNDIName('jms/NotificacaoQueue')
distQ.setSubDeploymentName('Stelo-DISTSubDeployment')

#CancelamentoPedidoComCompradorSemRisco
distQ=create('CancelamentoPedidoComCompradorSemRiscoQueue', 'UniformDistributedQueue')
distQ.setJNDIName('jms/CancelamentoPedidoComCompradorSemRiscoQueue')
distQ.setSubDeploymentName('Stelo-DISTSubDeployment')

#CancelamentoPedidoSemComprador
distQ=create('CancelamentoPedidoSemCompradorQueue', 'UniformDistributedQueue')
distQ.setJNDIName('jms/CancelamentoPedidoSemCompradorQueue')
distQ.setSubDeploymentName('Stelo-DISTSubDeployment')

cd('/')
cd('JMSSystemResource/PedidoJmsModule')
create('Stelo-DISTSubDeployment', 'SubDeployment')


cd('/')
assign('JMSServer', 'Stelo-JMSServer', 'Target', 'AdminServer')
assign('JMSSystemResource','PedidoJmsModule','Target','AdminServer')
assign('JMSSystemResource.SubDeployment', 'NotificacaoJmsModule.Stelo-SubDeployment', 'Target','Stelo-JMSServer')

updateDomain()
closeDomain()

exit()